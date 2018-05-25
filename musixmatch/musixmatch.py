import requests
import json

from .utils import _set_page_size


class Musixmatch(object):

    def __init__(self, apikey):
        ''' Define objects of type Musixmatch.
        Parameters:
        apikey - For get your apikey access: https://developer.musixmatch.com
        '''
        self.__apikey = apikey
        self.__url = 'http://api.musixmatch.com/ws/1.1/'

    def _get_url(self, url):
        return self.__url + '{}&apikey={}'.format(url, self._apikey)

    @property
    def _apikey(self):
        return self.__apikey

    def _request(self, url):
        data = requests.get(url).json()
        return data

    def chart_artists(self, page, page_size, country='us', _format='json'):
        ''' This api provides you the list
        of the top artists of a given country.
        Parameters:
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results (range 1 - 100).
        country - A valid country code (default US).
        format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('chart.artists.get?'
                                           'page={}&page_size={}'
                                           '&country={}&format={}'
                                           .format(page,
                                                   _set_page_size(page_size),
                                                   country, _format)))
        return data

    def chart_tracks_get(self, page, page_size, f_has_lyrics,
                         country='us', _format='json'):
        ''' This api provides you the list
        of the top songs of a given country.
        Parameters:
        page - Define the page number for paginated results.
        page_size - Define the page size for paginated results (range 1 - 100).
        f_has_lyrics - When set, filter only contents with lyrics.
        country - A valid country code (default US).
        format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('chart.tracks.get?'
                                           'page={}&page_size={}'
                                           '&country={}&format={}'
                                           '&f_has_lyrics={}'
                                           .format(page,
                                                   _set_page_size(page_size),
                                                   country, _format,
                                                   f_has_lyrics)))
        return data

    def track_search(self, q_track, q_artist, page_size, page,
                     s_track_rating, _format='json'):
        
        data = self._request(self._get_url('track.search?'
                                           'q_track={}&q_artist={}'
                                           '&page_size={}'
                                           '&page={}'
                                           '&s_track_rating={}&format={}'
                                           .format(q_track, q_artist,
                                                   _set_page_size(page_size),
                                                   page, s_track_rating,
                                                   _format)))
        return data

    def track_get(self, track_id, commontrack_id=None,
                  track_isrc=None, track_mbid=None, _format='json'):
        ''' Get a track info from our database:
        title, artist, instrumental flag and cover art.
        Parameters:
        track_id - The musiXmatch track id.
        commontrack_id - The musiXmatch commontrack id.
        track_isrc - A valid ISRC identifier.
        track_mbid - The musicbrainz recording id.
        format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('track.get?'
                                           'track_id={}&commontrack_id={}'
                                           '&track_isrc={}&track_mbid={}'
                                           '&format={}'
                                           .format(track_id, commontrack_id,
                                                   track_isrc, track_mbid,
                                                   _format)))
        return data

    def track_lyrics_get(self, track_id, track_mbid=None, _format='json'):
        ''' Get the lyrics of a track.
        Parameters:
        track_id - The musiXmatch track id.
        track_mbid - The musicbrainz track id.
        format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('track.lyrics.get?'
                                           'track_id={}&track_mbid={}'
                                           '&format={}'
                                           .format(track_id,
                                                   track_mbid, _format)))
        return data

    def track_snippet_get(self, track_id, _format='json'):
       
        data = self._request(self._get_url('track.snippet.get?'
                                           'track_id={}&format={}'
                                           .format(track_id, _format)))
        return data

    def track_subtitle_get(self, track_id, track_mbid=None,
                           subtitle_format=None, f_subtitle_length=None,
                           f_subtitle_length_max_deviation=None,
                           _format='json'):
        '''Retreive the subtitle of a track.
           Return the subtitle of a track in LRC or DFXP format.
           Refer to Wikipedia LRC format page or DFXP format on W3c
           for format specifications.
           Parameters:
           track_id - The musiXmatch track id.
           track_mbid - The musicbrainz track id.
           subtitle_format - The format of the subtitle (lrc,dfxp,stledu).
           Default to lrc.
           f_subtitle_length - The desired length of the subtitle (seconds).
           f_subtitle_length_max_deviation - The maximum deviation allowed.
           from the f_subtitle_length (seconds).
           format - Decide the output type json or xml (default json).
        '''
        data = self._request(self
                             ._get_url('track.subtitle.get?'
                                       'track_id={}&track_mbid={}'
                                       '&subtitle_format={}'
                                       '&f_subtitle_length={}'
                                       '&f_subtitle_length_max_deviation={}'
                                       '&format={}'
                                       .format(track_id,
                                               track_mbid,
                                               subtitle_format,
                                               f_subtitle_length,
                                               f_subtitle_length_max_deviation,
                                               _format)))
        return data

    def track_richsync_get(self, track_id, f_sync_length=None,
                           f_sync_length_max_deviation=None, _format='json'):
        '''Get the Rich sync for a track.
           A rich sync is an enhanced version of the
           standard sync which allows:
           - position offset by single characther.
           - endless formatting options at single char level.
           - multiple concurrent voices.
           - multiple scrolling direction.
           Parameters:
           track_id - The musiXmatch track id.
           f_sync_length - The desired length of the sync (seconds).
           f_sync_length_max_deviation - The maximum deviation allowed.
           from the f_sync_length (seconds).
        '''
        data = self._request(self._get_url('track.richsync.get?'
                                           'track_id={}&f_sync_length={}'
                                           '&f_sync_length_max_deviation={}'
                                           '&format={}'
                                           .format(track_id, f_sync_length,
                                                   f_sync_length_max_deviation,
                                                   _format)))
        return data

    def track_lyrics_post(self, track_id,
                          lyrics_body, _format='json'):
        
        data = self._request(self._get_url('track.lyrics.post?track_id={}'
                                           '&lyrics_body={}&format={}'
                                           .format(track_id, lyrics_body,
                                                   _format)))
        return data

    def track_lyrics_feedback_post(self, track_id, lyrics_id,
                                   feedback, _format='json'):
        ''' This API method provides you the opportunity to help
            us improving our catalogue.
            We aim to provide you with the best quality service imaginable,
            so we are especially interested in your detailed feedback to help
            us to continually improve it.
            Please take all the necessary precautions to avoid users or
            automatic software to use your website/app to use this commands,
            a captcha solution like http://www.google.com/recaptcha or an
            equivalent one has to be implemented in every user interaction that
            ends in a POST operation on the musixmatch api.
            Parameters:
            lyrics_id - The musiXmatch lyrics id.
            track_id - The musiXmatch track id.
            feedback - The feedback to be reported, possible values are:
            wrong_lyrics, wrong_attribution, bad_characters,
            lines_too_long, wrong_verses, wrong_formatting
            format - Decide the output type json or xml (default json)
        '''
        data = self._request(self._get_url('track.lyrics.feedback.post?'
                                           'track_id={}&lyrics_id={}'
                                           '&feedback={}&format={}'
                                           .format(track_id, lyrics_id,
                                                   feedback, _format)))
        return data

    def matcher_lyrics_get(self, q_track, q_artist, _format='json'):
        ''' Get the lyrics for track based on title and artist.
            Parameters:
            q_track - The song title
            q_artist - The song artist
            track_isrc - If you have an available isrc id in your catalogue
            you can query using this id only (optional)
            format - Decide the output type json or xml (default json)
        '''
        data = self._request(self._get_url('matcher.lyrics.get?'
                                           'q_track={}&q_artist={}&format={}'
                                           .format(q_track, q_artist,
                                                   _format)))
        return data

    def matcher_track_get(self, q_track, q_artist, _format='json'):
        
        data = self._request(self._get_url('matcher.track.get?'
                                           'q_track={}&q_artist={}'
                                           '&format={}'
                                           .format(q_track, q_artist,
                                                   _format)))
        return data

    def matcher_subtitle_get(self, q_track, q_artist, f_subtitle_length,
                             f_subtitle_length_max_deviation, track_isrc=None,
                             _format='json'):
        ''' Get the subtitles for a song given his title,artist and duration.
            You can use the f_subtitle_length_max_deviation to fetch subtitles
            within a given duration range.
            Parameters:
            q_track - The song title.
            q_artist - The song artist.
            f_subtitle_length - Filter by subtitle length in seconds.
            f_subtitle_length_max_deviation - Max deviation for a subtitle
            length in seconds.
            track_isrc - If you have an available isrc id in your catalogue
            you can query using this id only (optional).
            format - Decide the output type json or xml (default json).
            Note: This method requires a commercial plan.
        '''
        data = self._request(self
                             ._get_url('matcher.subtitle.get?q_track={}'
                                       '&q_artist={}&f_subtitle_length={}'
                                       '&f_subtitle_length_max_deviation={}'
                                       '&track_isrc={}&format={}'
                                       .format(q_track, q_artist,
                                               f_subtitle_length,
                                               f_subtitle_length_max_deviation,
                                               track_isrc,
                                               _format)))
        return data

    def artist_get(self, artist_id, artist_mbid=None, _format='json'):
        ''' Get the artist data from our database.
            Parameters:
            artist_id - Musixmatch artist id.
            artist_mbid - Musicbrainz artist id.
            format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('artist.get?artist_id={}'
                                           '&artist_mbid={}&format={}'
                                           .format(artist_id, artist_mbid,
                                                   _format)))
        return data

    def artist_search(self, q_artist, page, page_size, f_artist_id,
                      f_artist_mbid,
                      _format='json'):
        ''' Search for artists in our database.
            Parameters:
            q_artist - The song artist.
            f_artist_id - When set, filter by this artist id.
            f_artist_mbid - When set, filter by this artist musicbrainz id.
            page - Define the page number for paginated results.
            page_size - Define the page size for paginated results
            (Range is 1 to 100).
            format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('artist.search?q_artist={}'
                                           '&f_artist_id={}&f_artist_mbid={}'
                                           '&page={}&page_size={}&format={}'
                                           .format(q_artist, f_artist_id,
                                                   f_artist_mbid, page,
                                                   _set_page_size(page_size),
                                                   _format)))
        return data

    def artist_albums_get(self, artist_id, g_album_name, page, page_size,
                          s_release_date, artist_mbid=None, _format='json'):
        ''' Get the album discography of an artist.
            Parameters:
            artist_id - Musixmatch artist id.
            artist_mbid - Musicbrainz artist id.
            g_album_name - Group by Album Name.
            s_release_date - Sort by release date (asc|desc).
            page - Define the page number for paginated results.
            page_size - Define the page size for paginated results
            (range is 1 to 100).
            format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('artist.albums.get?artist_id={}'
                                           '&artist_mbid={}&g_album_name={}'
                                           '&s_release_date={}&page={}'
                                           '&page_size={}&format={}'
                                           .format(artist_id, artist_mbid,
                                                   g_album_name,
                                                   s_release_date,
                                                   page,
                                                   _set_page_size(page_size),
                                                   _format)))
        return data

    def artist_related_get(self, artist_id, page, page_size,
                           artist_mbid=None, _format='json'):
        ''' Get a list of artists somehow related to a given one.
            Parameters:
            artist_id - The musiXmatch artist id.
            artist_mbid - The musicbrainz artist id.
            page - Define the page number for paginated results.
            page_size - Define the page size for paginated results.
            (range is 1 to 100).
            format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('artist.related.get?artist_id={}'
                                           '&artist_mbid={}&page={}'
                                           '&page_size={}&format={}'
                                           .format(artist_id,
                                                   artist_mbid, page,
                                                   _set_page_size(page_size),
                                                   _format)))
        return data

    def album_get(self, album_id, _format='json'):
        ''' Get an album from our database:
            name, release_date, release_type, cover art.
            Parameters:
            album_id - The musiXmatch album id.
            format - Decide the output type json or xml (default json)
        '''
        data = self._request(self._get_url('album.get?album_id={}&format={}'
                                           .format(album_id, _format)))
        return data

    def album_tracks_get(self, album_id, page, page_size, album_mbid,
                         f_has_lyrics=None, _format='json'):
        ''' This api provides you the list of the songs of an album.
            Parameters:
            album_id - Musixmatch album id.
            album_mbid - Musicbrainz album id.
            f_has_lyrics - When set, filter only contents with lyrics.
            page - Define the page number for paginated results.
            page_size - Define the page size for paginated results.
            (range is 1 to 100).
            format - Decide the output type json or xml (default json).
        '''
        data = self._request(self._get_url('album.tracks.get?album_id={}'
                                           '&album_mbid={}&f_has_lyrics={}'
                                           '&page={}&page_size={}&format={}'
                                           .format(album_id, album_mbid,
                                                   f_has_lyrics, page,
                                                   _set_page_size(page_size),
                                                   _format)))
        return data

    def tracking_url_get(self, domain, _format='json'):
        
        data = self._request(self._get_url('tracking.url.get?'
                                           'domain={}&format={}'
                                           .format(domain, _format)))
        return data

    def catalogue_dump_get(self, url):
        ''' Get the list of our songs with the lyrics last updated information.
            CATALOGUE_COMMONTRACKS
            Dump of our catalogue in this format:
            {
                "track_name": "Shape of you",
                "artist_name": "Ed Sheeran",
                "commontrack_id":12075763,
                "instrumental": false,
                "has_lyrics": yes,
                "updated_time": "2013-04-08T09:28:40Z"
            }
            Note: This method requires a commercial plan.
        '''
        data = self._request(self._get_url(url))
        return data