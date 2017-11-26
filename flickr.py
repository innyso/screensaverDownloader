#!/usr/bin/env python3

"""screensaver_downloader

Usage:
    screensaver_downloader.py [--apikey=<key>]
                              [--apisecret=<secret>]
                              [--outputdir=<outputdir>]
                              [--userid=<userid>]

Options:
  -h --help     Show this screen.
  --apikey=<key>      flickr api key
  --apisecret=<secret>   flickr api secret
  --outputdir=<outputdir> output directory
  --userid flickr userid

"""

import flickrapi as flickr
import docopt
import requests
import os

arguments = docopt.docopt(__doc__)
api_key = arguments['--apikey']
api_secret = arguments['--apisecret']
output_dir = arguments['--outputdir']
user_id = arguments['--userid']

print("running flickr downloader")
flickrClient = flickr.FlickrAPI(api_key, api_secret, format='parsed-json')
photos = flickrClient.photos.search(
        user_id=user_id,
        per_page='50',
        tags=['screensaver'],
        extras=['url_o'])

new_photo = list(filter(lambda x: not (os.path.exists(os.path.join(output_dir, x['id'] + '.jpg'))), photos['photos']['photo']))
for photo in new_photo:
    filename = "%s.jpg" % (photo['id'])
    output_path = os.path.join(output_dir, filename)
    print("downloading %s to %s" % (filename, output_path))
    file = requests.get(photo['url_o'], allow_redirects=True)
    open(output_path, 'wb').write(file.content)
