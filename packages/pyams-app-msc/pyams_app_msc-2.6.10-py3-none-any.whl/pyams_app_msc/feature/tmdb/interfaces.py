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

"""PyAMS_app_msc.feature.tmdb interfaces module

"""

from zope.interface import Interface, Invalid, invariant
from zope.schema import Bool, Choice, Int, Object, TextLine, URI

from pyams_i18n.interfaces import ISO_LANGUAGES_VOCABULARY_NAME
from pyams_utils.interfaces.proxy import IProxyInfo

__docformat__ = 'restructuredtext'

from pyams_app_msc import _


TMDB_SEARCH_ROUTE = 'pyams_msc.tmdb.search'
'''TMDB search API route'''

TMDB_SEARCH_PATH = '/api/msc/tmdb'
'''TMDB search API default path'''

TMDB_CONFIGURATION_KEY = 'msc.tmdb.configuration'
'''TMDB configuration annotations key'''


class ITMDBConfiguration(Interface):
    """TMDB configuration interface"""

    enabled = Bool(title=_("Enable TMDB configuration"),
                   required=True,
                   default=False)

    service_url = URI(title=_("Service URL"),
                      description=_("Main TMDB services base URL"),
                      required=False,
                      default="https://api.themoviedb.org")

    proxy_info = Object(title=_("Proxy information"),
                        description=_("Enter information if a proxy is required"),
                        required=False,
                        schema=IProxyInfo)

    def get_proxy_info(self, request=None, protocol=None):
        """Proxy information getter"""

    api_key = TextLine(title=_("API key"),
                       description=_("API authentication key (v3)"),
                       required=False)

    bearer_token = TextLine(title=_("Bearer token"),
                            description=_("Bearer authentication token (v4)"),
                            required=False)

    @invariant
    def check_api_key(self):
        """API key checker"""
        if self.enabled and not (self.api_key or self.bearer_token):
            raise Invalid(_("You must define an API key or a Bearer token to enable TMDB configuration!"))

    language = Choice(title=_("Language"),
                      description=_("Primary language used for TMDB API"),
                      vocabulary=ISO_LANGUAGES_VOCABULARY_NAME,
                      required=False,
                      default='en-US')

    movie_search_path = TextLine(title=_("Movie search path"),
                                 description=_("Path to TMDB movie search API"),
                                 required=False,
                                 default='/3/search/movie')

    movie_details_path = TextLine(title=_("Movie details path"),
                                  description=_("Path to TMDB movie details API, including {movie_id} argument"),
                                  required=False,
                                  default='/3/movie/{movie_id}')

    movie_credits_path = TextLine(title=_("Movie credits path"),
                                  description=_("Path to TMDB movie credits API, including {movie_id} argument"),
                                  required=False,
                                  default='/3/movie/{movie_id}/credits')

    actors_count = Int(title=_("Actors count"),
                       description=_("Number of actors "),
                       required=False,
                       default=4)

    movie_images_path = TextLine(title=_("Movie images path"),
                                 description=_("Path to TMDB movie images API, including {movie_id} argument"),
                                 required=False,
                                 default='/3/movie/{movie_id}/images')

    movie_videos_path = TextLine(title=_("Movie videos path"),
                                 description=_("Path to TMDB movie videos API, including {movie_id} argument"),
                                 required=False,
                                 default='/3/movie/{movie_id}/videos')

    images_url = URI(title=_("Images URL"),
                     description=_("TMDB images base URL, including {size} and {image_id} arguments"),
                     required=False,
                     default="https://image.tmdb.org/t/p/{size}{image_id}")

    download_main_poster = Bool(title=_("Download main poster?"),
                                description=_("If 'no', movie poster will not be downloaded on activity creation"),
                                required=True,
                                default=True)

    main_poster_size = Choice(title=_("Main poster size"),
                              description=_("This is the size of poster image downloaded from TMDB"),
                              values=('w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original'),
                              default='w780',
                              required=False)

    download_pictures = Bool(title=_("Download pictures?"),
                             description=_("If 'no', movie pictures will not be downloaded on activity creation"),
                             required=True,
                             default=True)

    pictures_size = Choice(title=_("Pictures size"),
                           description=_("This is the size of movies images downloaded from TMDB"),
                           values=('w300', 'w780', 'w1280', 'original'),
                           default='w780',
                           required=False)

    download_posters = Bool(title=_("Download posters?"),
                            description=_("If 'no', movie posters will not be downloaded on activity creation"),
                            required=True,
                            default=True)

    posters_size = Choice(title=_("Posters size"),
                          description=_("This is the size of posters images downloaded from TMDB"),
                          values=('w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original'),
                          default='w780',
                          required=False)

    download_videos = Bool(title=_("Download videos?"),
                           description=_("If 'no', movie videos will not be downloaded on activity creation"),
                           required=True,
                           default=True)

    restrict_videos_language = Bool(title=_("Get videos for selected language only"),
                                    description=_("If 'yes', only videos tagged for selected language will "
                                                  "be selected; otherwise, other videos tagged for any language "
                                                  "may also be selected"),
                                    required=True,
                                    default=True)


class ITMDBService(Interface):
    """TMDB service interface"""

    def find_movies(self, query: str):
        """Find movies matching provided query"""

    def get_movie_info(self, movie_id: int):
        """Get detailed information about movie identified by its TMDB ID"""

    def get_movie_pictures(self, movie_id: int):
        """Get pictures of movie identified by its TMDB ID"""

    def set_activity_info(self, activity):
        """Set TMDB information for provided activity"""


class ITMDBServiceClientTarget(Interface):
    """TMDB service client target marker interface

    This interface is used to tag components which can use TMDB service
    to get information about a given movie.
    """
