#!/usr/bin/env python
#
# Copyright 2013-2014 Sergio Arroutbi Braojos <sarroutbi@yahoo.es>
# 
# Permission to use, copy, modify, and/or distribute this software 
# for any purpose with or without fee is hereby granted, provided that 
# the above copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES 
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY 
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, 
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH 
# THE USE OR PERFORMANCE OF THIS SOFTWARE
#
from bs4 import BeautifulSoup as Soup
import geturl
import sys

def print_urls(url):
    text = geturl.urlToString(url)
    try:
        s = Soup(text)
        return [x['href'] for x in s.findAll('a', href=True)]
    except:
        print "ERROR ON SOUP CREATION"
        return []

def print_links_to_level(url, max_depth):
    print_child_list(url, 1)
    recursive_analyze_links(url, 2, max_depth)
    
def recursive_analyze_links(url, depth, max_depth):
    url_list = print_urls(url)
    if depth <= max_depth:
        for l in url_list:
            print_child_list(l, depth)
        for l in url_list:
            recursive_analyze_links(l, depth+1, max_depth)

def print_child_list(url, depth):
    url_list = print_urls(url)
    for l in url_list:
        print_depth_point(depth)
        print " %s" % (l)

def print_depth_point(depth):
    counter = 0
    while counter < depth:
        sys.stdout.write("*")
        sys.stdout.flush()
        counter+=1
