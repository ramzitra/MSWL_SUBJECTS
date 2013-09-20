#!/usr/bin/env python
#
# TODO: FILL LICENSE INFORMATION
# (c) 2013 Sergio Arroutbi
#
import sys
import pyarsespyder
import argparse

def main ():

    parser = argparse.ArgumentParser(description='Internet Crawler',
                                     version = '0.0-1')
    parser.add_argument('-n', '--number-of-levels',
                        type = int, default = 1, help = 'Crawling depth')
    parser.add_argument('url', nargs=1, help = 'URL to crawl')

    args = parser.parse_args()
                        
    # number_of_levels because the long parameter
    # is called "--number-of-levels"
    depth = args.number_of_levels

    url = args.url

    print_links(url[0], 1, depth)

def print_links(url, depth, max_depth):
    url_list = pyarsespyder.print_urls(url)

    if depth <= max_depth:
        for l in url_list:
            print_depth_point(depth)
            print " %s" % (l)
        for l in url_list:
            print_links(l, depth+1, max_depth)

def print_depth_point(depth):
    counter = 0
    while counter < depth:
        sys.stdout.write("*")
        sys.stdout.flush()
        counter+=1
    
if __name__ == '__main__':
    main()
