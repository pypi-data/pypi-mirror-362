# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import csv
import logging
import subprocess
import pkg_resources
from io import StringIO

try:
    from urllib.parse import urlparse
    from urllib.parse import urlunparse
    from urllib.parse import urlencode
    from urllib.error import HTTPError
    from urllib import request
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.request import build_opener
    from urllib.request import install_opener
    from urllib.request import BaseHandler
    from email.message import Message
except ImportError:
    from urlparse import urlparse
    from urlparse import urlunparse
    from urllib import urlencode
    from urllib2 import HTTPError
    import urllib2 as request
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import build_opener
    from urllib2 import install_opener
    from urllib2 import BaseHandler
    from email.Message import Message

from zc.buildout import download

log = logging.getLogger('p01.buildouthttp')
original_build_opener = build_opener


def retrieve_url(url, filename=None, data=None):
    req = Request(url, data=data)
    try:
        response = urlopen(req)
        content = response.read()
        if filename:
            with open(filename, 'wb') as f:
                f.write(content)
        return (filename or url, response.info())
    except HTTPError as err:
        log.error('failed to get url: %r %r', url, err.code)
        raise


def isPrivate(urlPath, repos):
    if repos is None:
        return True
    for repo in repos:
        if not repo:
            continue
        api_repo = "/repos/%s/" % repo
        dl_repo = "/downloads/%s/" % repo
        if api_repo in urlPath or dl_repo in urlPath:
            return True
    return False


class GithubHandler(BaseHandler):
    """This handler creates a post request with login and token

    see http://github.com/blog/170-token-authentication for details

    With a none github url the resulting request is unchanged::

    >>> req = request.Request('http://example.com/downloads/me/')
    >>> handler = GithubHandler('--mytoken--')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'http://example.com/downloads/me/'
    >>> res is req
    True

    With a github url we get the access token::

    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?access_token=--mytoken--'

    If we provide an empty whitelist we get all github requests without a
    token::

    >>> handler = GithubHandler('--mytoken--', [])
    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/'

    If the repository is in the whitelist is receives a token::

    >>> handler = GithubHandler('--mytoken--', ['me'])
    >>> req = request.Request('https://github.com/downloads/me/')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?access_token=--mytoken--'

    >>> req = request.Request(
    ...           'https://github.com/downloads/me/?a=1&b=2')
    >>> res = handler.https_request(req)
    >>> res.get_full_url()
    'https://github.com/downloads/me/?a=1&b=2&access_token=--mytoken--'

    If no timeout is set in the original request, the timeout is set to 60::

    >>> hasattr(req, 'timeout')
    False
    >>> res.timeout
    60


    The timeout from the original request is preseverd in the result::

    >>> req = request.Request('https://github.com/downloads/me/?a=1&b=2')
    >>> req.timeout = 42
    >>> res = handler.https_request(req)
    >>> res.timeout
    42

    """

    def __init__(self, token, repos=None):
        self._token = token
        self._repos = repos

    def https_request(self, req):
        host = req.get_host() if hasattr(req, "get_host") else req.host
        if req.get_method() == 'GET' and host.endswith('github.com'):
            url = req.get_full_url()
            scheme, netloc, path, params, query, fragment = urlparse(url)
            if isPrivate(path, self._repos):
                log.debug("Found private github url %r", url)
                token = urlencode(dict(access_token=self._token))
                query = '&'.join([p for p in (query, token) if p])
                new_url = urlunparse((scheme, netloc, path, params, query, fragment))
                timeout = getattr(req, 'timeout', 60)
                old_req = req
                req = Request(new_url)
                req.timeout = timeout
                req.add_header('user-agent', old_req.get_header('user-agent', 'Python-urllib2'))
            else:
                log.debug("Github url %r blocked by buildout.github-repos", url)
                log.debug(self._repos)
        return req


class CredHandler(request.HTTPBasicAuthHandler):
    def http_error_401(self, req, fp, code, msg, headers):
        try:
            self.retried = 0
        except AttributeError:
            pass

        log.debug('getting url: %r' % req.get_full_url())
        try:
            res = request.HTTPBasicAuthHandler.http_error_401(
                self, req, fp, code, msg, headers)
        except HTTPError as err:
            log.error('failed to get url: %r %r', req.get_full_url(), err.code)
            raise
        except Exception as err:
            log.error('failed to get url: %r %s', req.get_full_url(), str(err))
            raise
        else:
            if res is None:
                log.error('failed to get url: %r, check your realm', req.get_full_url())
            elif res.code >= 400:
                log.error('failed to get url: %r %r', res.url, res.code)
            else:
                log.debug('got url: %r %r', res.url, res.code)
            return res


def prompt_passwd(realm, user):
    from getpass import getpass
    return getpass('>>> Password for {} - {}: '.format(realm, user))


def set_up_opener(creds, github_creds, github_repos):
    handlers = []
    if github_creds:
        handlers.append(GithubHandler(github_creds, github_repos))
    if creds:
        auth_handler = CredHandler()
        for realm, uris, user, password in creds:
            auth_handler.add_password(realm, uris, user, password)
        handlers.append(auth_handler)
    opener = build_opener(*handlers)
    install_opener(opener)


def get_github_credentials():
    p = subprocess.Popen(
        "git config github.accesstoken",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    rc = p.wait()
    if rc:
        return None
    token = p.stdout.readline().strip()
    p.stdout.close()
    p.stderr.close()
    if token:
        log.debug("Found github accesstoken %r", token)
        return token



def install(buildout=None, pwd_path=None):
    pwdsf = StringIO()
    combined_creds = []
    github_creds = None
    creds = []
    local_pwd_path = ''
    home_path = ''
    github_repos = None

    if buildout is not None:
        local_pwd_path = os.path.join(buildout['buildout']['directory'], '.httpauth')
        if 'github-repos' in buildout['buildout']:
            github_repos = buildout['buildout']['github-repos'].split('\n')

    system_pwd_path = os.path.join(os.path.expanduser('~'), '.buildout', '.httpauth')
    home = os.environ.get('HOME') or os.environ.get('USERPROFILE')
    if home is not None:
        home_path = os.path.join(home, '.buildout', '.httpauth')

    def combine_cred_file(file_path):
        if file_path and os.path.exists(file_path):
            with open(file_path) as f:
                combined_creds.extend([l.strip() for l in f if l.strip()])

    combine_cred_file(pwd_path)
    combine_cred_file(local_pwd_path)
    combine_cred_file(system_pwd_path)
    combine_cred_file(home_path)

    pwdsf_len = pwdsf.write(u"\n".join(combined_creds))
    pwdsf.seek(0)

    if not pwdsf_len:
        pwdsf = None
        log.warning('Could not load authentication information')

    try:
        github_creds = get_github_credentials()
        if pwdsf:
            for l, row in enumerate(csv.reader(pwdsf)):
                if len(row) == 3:
                    realm, uris, user = (el.strip() for el in row)
                    password = prompt_passwd(realm, user)
                elif len(row) == 4:
                    realm, uris, user, password = (el.strip() for el in row)
                else:
                    raise RuntimeError("Authentication file cannot be parsed %s:%s" % (pwd_path, l + 1))
                creds.append((realm, uris, user, password))
                log.debug('Added credentials %r, %r' % (realm, uris))
        if creds or github_creds:
            set_up_opener(creds, github_creds, github_repos)
    finally:
        if pwdsf:
            pwdsf.close()


def unload(buildout=None):
    request.build_opener = original_build_opener
    request.install_opener(request.build_opener())