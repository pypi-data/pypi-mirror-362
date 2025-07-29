#
# Copyright (c) 2015-2023 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

import importlib
from datetime import date
from typing import Iterable, Optional

import requests
from persistent import Persistent
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPOk
from zope.container.contained import Contained
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.schema.fieldproperty import FieldProperty

from pyams_app_msc.feature.tmdb.interfaces import ITMDBConfiguration, ITMDBService, ITMDBServiceClientTarget, \
    TMDB_CONFIGURATION_KEY
from pyams_content.component.gallery.interfaces import GALLERY_PARAGRAPH_TYPE, IGalleryFile, IGalleryParagraph
from pyams_content.component.illustration.interfaces import IIllustration
from pyams_content.component.paragraph.interfaces import IParagraphContainer
from pyams_content.component.video import external_video_settings
from pyams_content.component.video.interfaces import IExternalVideoParagraph
from pyams_i18n.interfaces import II18n, INegotiator
from pyams_site.interfaces import ISiteRoot
from pyams_utils.adapter import adapter_config, get_annotation_adapter
from pyams_utils.country import ISO_COUNTRIES
from pyams_utils.factory import create_object, factory_config, get_object_factory
from pyams_utils.registry import get_utility
from pyams_utils.request import check_request
from pyams_utils.url import generate_url


@factory_config(ITMDBConfiguration)
class TMDBConfiguration(Persistent, Contained):
    """TMDB configuration persistent class"""

    enabled = FieldProperty(ITMDBConfiguration['enabled'])
    service_url = FieldProperty(ITMDBConfiguration['service_url'])
    proxy_info = FieldProperty(ITMDBConfiguration['proxy_info'])
    api_key = FieldProperty(ITMDBConfiguration['api_key'])
    bearer_token = FieldProperty(ITMDBConfiguration['bearer_token'])
    language = FieldProperty(ITMDBConfiguration['language'])
    movie_search_path = FieldProperty(ITMDBConfiguration['movie_search_path'])
    movie_details_path = FieldProperty(ITMDBConfiguration['movie_details_path'])
    movie_credits_path = FieldProperty(ITMDBConfiguration['movie_credits_path'])
    actors_count = FieldProperty(ITMDBConfiguration['actors_count'])
    movie_images_path = FieldProperty(ITMDBConfiguration['movie_images_path'])
    movie_videos_path = FieldProperty(ITMDBConfiguration['movie_videos_path'])
    images_url = FieldProperty(ITMDBConfiguration['images_url'])
    download_main_poster = FieldProperty(ITMDBConfiguration['download_main_poster'])
    main_poster_size = FieldProperty(ITMDBConfiguration['main_poster_size'])
    download_pictures = FieldProperty(ITMDBConfiguration['download_pictures'])
    pictures_size = FieldProperty(ITMDBConfiguration['pictures_size'])
    download_posters = FieldProperty(ITMDBConfiguration['download_posters'])
    posters_size = FieldProperty(ITMDBConfiguration['posters_size'])
    download_videos = FieldProperty(ITMDBConfiguration['download_videos'])
    restrict_videos_language = FieldProperty(ITMDBConfiguration['restrict_videos_language'])

    def get_proxy_info(self, request=None, protocol=None):
        """Proxy information getter"""
        info = self.proxy_info
        if not info:
            return {}
        if request is None:
            request = check_request()
        url = info.get_proxy_url(request)
        if not url:
            return {}
        if protocol is None:
            protocol = request.scheme
        return {protocol: url}


@adapter_config(required=ISiteRoot,
                provides=ITMDBConfiguration)
def tmdb_configuration(context):
    """TMDB configuration adapter"""
    return get_annotation_adapter(context, TMDB_CONFIGURATION_KEY, ITMDBConfiguration)


@factory_config(ITMDBService)
class TMDBService:
    """Default TMDB service implementation"""

    @reify
    def configuration(self) -> Optional[ITMDBConfiguration]:
        """Configuration getter"""
        request = check_request()
        configuration = ITMDBConfiguration(request.root, None)
        if (configuration is None) or not configuration.enabled:
            return None
        return configuration

    @staticmethod
    def get_data(configuration: ITMDBConfiguration, path: str, params: dict) -> dict:
        """HTTP request getter"""
        headers = {
            'accept': 'application/json'
        }
        if 'language' not in params:
            params['language'] = configuration.language
        if configuration.bearer_token:
            headers['Authorization'] = f'Bearer {configuration.bearer_token}'
        else:
            params['api_key'] = configuration.api_key
        url = f'{configuration.service_url}{path}'
        response = requests.get(url, params=params, headers=headers,
                                proxies=configuration.get_proxy_info(protocol='https'))
        if response.status_code == HTTPOk.code:
            return response.json()
        return {}

    @staticmethod
    def get_image(configuration: ITMDBConfiguration, image_id: str, size: str) -> Optional[bytes]:
        """HTTP image getter"""
        url = configuration.images_url.format(size=size, image_id=image_id)
        response = requests.get(url, proxies=configuration.get_proxy_info(protocol='https'))
        if response.status_code == HTTPOk.code:
            return response.content
        return None

    def find_movies(self, query: str) -> Iterable:
        """Find movies in TMDB database"""
        configuration = self.configuration
        if configuration is None:
            return
        # check language
        lang = None
        if ':' in query:
            lang, query = query.split(':', 1)
        # check release year
        year = None
        if ',' in query:
            title, year = map(str.strip, query.rsplit(',', 1))
            try:
                year = int(year)
            except ValueError:
                title = query
                year = None
        else:
            title = query
        params = {
            'query': title
        }
        if lang:
            params['language'] = lang
        if year:
            params['year'] = year
        for result in self.get_data(configuration, configuration.movie_search_path, params) \
                .get('results', ()):
            if 'release_date' in result:
                try:
                    release_year = date.fromisoformat(result['release_date']).year
                except ValueError:
                    release_year = None
            else:
                release_year = None
            yield {
                'movie_id': result.get('id'),
                'title': result.get('title'),
                'release_year': release_year
            }

    def get_movie_info(self, movie_id: int, with_credits=True) -> Optional[dict]:
        """Get detailed information about movie identified by its TMDB ID"""

        configuration = self.configuration
        if configuration is None:
            return
        response = self.get_data(configuration,
                                 configuration.movie_details_path.format(movie_id=movie_id), {})
        if response is None:
            return
        request = check_request()
        translate = request.localizer.translate
        result = {
            'id': response.get('id'),
            'title': response.get('title'),
            'duration': response.get('runtime'),
            'release_year': date.fromisoformat(response.get('release_date')).year,
            'original_country': ', '.join((
                translate(ISO_COUNTRIES.get(item.get('iso_3166_1')))
                for item in response.get('production_countries')
            )),
            'original_title': response.get('original_title'),
            'original_language': response.get('original_language'),
            'poster_id': response.get('poster_path'),
            'overview': response.get('overview')
        }
        if with_credits:
            response = self.get_data(configuration,
                                     configuration.movie_credits_path.format(movie_id=movie_id), {})
            if response is not None:
                actors = []
                for index, cast in enumerate(response.get('cast', ())):
                    actors.append(cast.get('name'))
                    if index >= configuration.actors_count - 1:
                        break
                result['actors'] = ', '.join(actors)
                producers = []
                writers = []
                directors = []
                composers = []
                for crew in response.get('crew', ()):
                    job = crew.get('job')
                    name = crew.get('name')
                    if job == 'Producer':
                        producers.append(name)
                    elif job in ('Screenplay', 'Writer'):
                        writers.append(name)
                    elif job == 'Director':
                        directors.append(name)
                    elif job == 'Original Music Composer':
                        composers.append(name)
                result['producers'] = ', '.join(producers)
                result['writers'] = ', '.join(writers)
                result['directors'] = ', '.join(directors)
                result['composers'] = ', '.join(composers)
        return result

    def get_movie_pictures(self, movie_id: int, lang: str) -> Optional[Iterable]:
        """Get pictures of movie identified by its TMDB ID"""
        configuration = self.configuration
        if configuration is None:
            return
        response = self.get_data(configuration,
                                 configuration.movie_images_path.format(movie_id=movie_id), {
                                     'include_image_language': f'{lang},null'
                                 })
        if response is not None:
            for image in response.get('backdrops', ()):
                yield {
                    'image_type': 'backdrop',
                    'image_id': image.get('file_path')
                }
            for image in response.get('posters', ()):
                yield {
                    'image_type': 'poster',
                    'image_id': image.get('file_path')
                }

    def get_movie_videos(self, movie_id: int, lang: str) -> Optional[Iterable]:
        """Get videos of movie identified by its TMDB ID"""
        configuration = self.configuration
        if configuration is None:
            return
        response = self.get_data(configuration,
                                 configuration.movie_videos_path.format(movie_id=movie_id), {
                                     'language': lang if configuration.restrict_videos_language else f'{lang},null'
                                 })
        if response is not None:
            for video in response.get('results', ()):
                yield {
                    'video_type': video.get('site'),
                    'video_id': video.get('key'),
                    'title': video.get('name'),
                    'type': video.get('type')
                }

    def set_activity_info(self, activity) -> None:
        """Get TMDB information for provided activity"""
        configuration = self.configuration
        if configuration is None:
            return
        movie_id = activity.tmdb_movie_id
        if not movie_id:
            title = II18n(activity).query_attribute('title', request=check_request())
            for movie in self.find_movies(title):
                movie_id = movie.get('movie_id')
        if movie_id:
            negotiator = get_utility(INegotiator)
            info = self.get_movie_info(movie_id)
            if info is None:
                return
            # set activity properties
            title = info.get('title')
            activity.title = {
                negotiator.server_language: title
            }
            activity.content_url = generate_url(title)
            # set illustration
            if configuration.download_main_poster:
                illustration = IIllustration(activity, None)
                if illustration is not None:
                    illustration.data = {
                        negotiator.server_language: self.get_image(configuration,
                                                                   image_id=info.get('poster_id'),
                                                                   size=configuration.main_poster_size)
                    }
            # set activity info
            interfaces = importlib.import_module('pyams_app_msc.shared.catalog.interfaces')
            catalog_info = interfaces.ICatalogEntryInfo(activity, None)
            if catalog_info is not None:
                catalog_info.tmdb_id = info.get('id')
                catalog_info.release_year = info.get('release_year')
                catalog_info.original_country = info.get('original_country')
                catalog_info.original_title = info.get('original_title')
                catalog_info.original_language = info.get('original_language')
                catalog_info.producer = info.get('producers')
                catalog_info.writer = info.get('writers')
                catalog_info.director = info.get('directors')
                catalog_info.composer = info.get('composers')
                catalog_info.actors = info.get('actors')
                catalog_info.duration = info.get('duration')
                catalog_info.synopsis = info.get('overview')
            # set gallery images
            if configuration.download_pictures or configuration.download_posters:
                paragraphs = IParagraphContainer(activity, None)
                if paragraphs is not None:
                    gallery_file_factory = get_object_factory(IGalleryFile)
                    if gallery_file_factory is not None:
                        galleries = list(paragraphs.get_paragraphs(GALLERY_PARAGRAPH_TYPE))
                        if galleries:
                            gallery = galleries[0]
                        else:
                            gallery = create_object(IGalleryParagraph)
                            paragraphs.append(gallery)
                        for picture in self.get_movie_pictures(movie_id, negotiator.server_language):
                            image_type = picture.get('image_type')
                            if (image_type == 'backdrop') and not configuration.download_pictures:
                                continue
                            if (image_type == 'poster') and not configuration.download_posters:
                                continue
                            gallery_file = gallery_file_factory()
                            gallery.append(gallery_file)
                            gallery_file.visible = False
                            if image_type == 'poster':
                                gallery_file.data = self.get_image(configuration,
                                                                   image_id=picture.get('image_id'),
                                                                   size=configuration.posters_size)
                            else:
                                gallery_file.data = self.get_image(configuration,
                                                                   image_id=picture.get('image_id'),
                                                                   size=configuration.pictures_size)
            # set videos
            if configuration.download_videos:
                paragraphs = IParagraphContainer(activity, None)
                if paragraphs is not None:
                    video_factory = get_object_factory(IExternalVideoParagraph)
                    if video_factory is not None:
                        for video in self.get_movie_videos(movie_id, configuration.language):
                            paragraph = video_factory()
                            paragraph.visible = False
                            paragraph.title = {
                                negotiator.server_language: video.get('title')
                            }
                            paragraph.description = {
                                negotiator.server_language: video.get('type')
                            }
                            paragraph.author = video.get('video_type')
                            paragraph.provider_name = video.get('video_type', '').lower()
                            paragraphs.append(paragraph)
                            settings = external_video_settings(paragraph)
                            settings.video_id = video.get('video_id')


@subscriber(IObjectAddedEvent, context_selector=ITMDBServiceClientTarget)
def handle_added_catalog_entry(event):
    """Check TMDB lookup when catalog entry is created"""
    request = check_request()
    tmdb_lookup = request.params.get('form.widgets.tmdb_lookup')
    if not tmdb_lookup:
        return
    tmdb_service = create_object(ITMDBService)
    if tmdb_service is None:
        return
    tmdb_service.set_activity_info(event.object)
