from collections.abc import Iterable
from http import HTTPMethod
from logging import Logger, LoggerAdapter, getLogger
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote, urljoin

import aiofiles
import aiohttp
import yarl

import cafs_cache_cdn_client.repo.datatypes as dt

__all__ = ('RepoClient',)


module_logger = getLogger(__name__)


class RepoClient:
    server_base_url: str
    logger: Logger | LoggerAdapter

    def __init__(
        self, server: str, logger: Logger | LoggerAdapter | None = None
    ) -> None:
        self.server_base_url = server
        self.logger = logger or module_logger

    async def _request(
        self,
        endpoint: str,
        params: Iterable[tuple[str, str]] | None = None,
        method: HTTPMethod = HTTPMethod.GET,
        data: dict | bytes | aiohttp.FormData | None = None,
        headers: dict[str, str] | None = None,
        json_request: bool = True,
    ) -> Any:
        if params:
            endpoint += '?' + '&'.join(f'{k}={quote(v)}' for k, v in params)
        headers = headers.copy() if headers else {}
        if json_request:
            headers['Content-Type'] = 'application/json'
        url_ = yarl.URL(urljoin(self.server_base_url, endpoint), encoded=True)
        if json_request:
            data_arg = {'json': data}
        else:
            data_arg = {'data': data}
        self.logger.debug('Requesting %s', url_)
        async with aiohttp.ClientSession(
            headers=headers, requote_redirect_url=False
        ) as session:
            async with session.request(
                method, url_, **data_arg, raise_for_status=True
            ) as resp:
                if resp.headers.get('Content-Type') == 'application/json':
                    return await resp.json()
                return await resp.read()

    async def get_settings(self) -> dt.SettingsResponse:
        return cast(
            dt.SettingsResponse, await self._request('/settings', method=HTTPMethod.GET)
        )

    async def get_blob_urls(self) -> list[str]:
        settings = await self.get_settings()
        return settings['blob_urls']

    async def is_ref_exist(self, repo: str, ref: str) -> bool:
        try:
            await self._request(f'/repository/{repo}/{ref}', method=HTTPMethod.HEAD)
            return True
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                return False
            raise

    async def delete_ref(self, repo: str, ref: str) -> None:
        try:
            await self._request(f'/repository/{repo}/{ref}', method=HTTPMethod.DELETE)
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                return
            raise

    async def get_ref_info(self, repo: str, ref: str) -> dt.RefInfoResponse:
        return cast(
            dt.RefInfoResponse,
            await self._request(f'/repository/{repo}/{ref}', method=HTTPMethod.GET),
        )

    async def tag_ref(self, repo: str, ref: str, tag: str) -> None:
        await self._request(
            f'/repository/{repo}/{ref}/tag', method=HTTPMethod.POST, data={'tag': tag}
        )

    async def post_ref_info(self, repo: str, ref: str, data: dt.RefInfoBody) -> None:
        await self._request(
            f'/repository/{repo}/{ref}', method=HTTPMethod.POST, data=data
        )

    async def attach_file(self, repo: str, ref: str, file_path: Path) -> None:
        async with aiofiles.open(file_path, 'rb') as f:
            form_data = aiohttp.FormData()
            form_data.add_field('file', f, filename=file_path.name)
            await self._request(
                f'/repository/{repo}/{ref}/attach',
                method=HTTPMethod.POST,
                data=form_data,
                json_request=False,
            )
