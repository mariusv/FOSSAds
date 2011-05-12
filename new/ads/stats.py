# -*- coding: utf-8 -*-
# This file is part of cuZmeură.
# Copyright (c) 2009-2010 Ionuț Arțăriși

# cuZmeură is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.

# cuZmeură is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with cuZmeură.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.db import connection, transaction
from django.http import HttpResponse
from ads.models import Ad, Impression, Product, User

import cairo
import pycha.line
from datetime import datetime

def graph_monthly_imp(publisher):
    '''Draw a graph of the last month Impressions of a given Publisher
    Returns a png image
    '''
    # There is a time for ugly SQL (I would love to have this rewritten)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT EXTRACT(day FROM timestamp) AS days,
            COUNT(EXTRACT(day FROM timestamp))
         FROM ads_impression
         WHERE age(timestamp) < interval '30 days' AND publisher = %s
         GROUP BY days ORDER BY days;
         """, [publisher.url])
    rows = cursor.fetchall()
    cursor.close()

    # make sure that all the days are represented, even if they don't have an
    # impression in the db
    days = dict([(d, 0) for d in range(1, 31)])
    days.update(rows)
    rows = days.items()
    
    # split in two months at current day, but leave the rows the same, because
    # pycha expects them to be ordered when drawing the graph
    today = datetime.today().day
    ticks = rows[today-1:] + rows[:today-1]

    # keep the rows in the right order
    # [(29, 1), (30, 2), (7, 41), (8, 42), (9, 43) etc. becomes:
    # [(1, 1), (2, 2), (3, 41), (4, 42), (5, 43) etc.
    rows = [(ticks.index((i, j)), j) for i, j in ticks]

    # pycha expects this to be a list of dicts like {Xaxis value: label}
    ticks = [dict(v=i, label=int(l[0])) for i, l in enumerate(ticks)]
    
    # fetchall returns tuples of floats for day numbers,
    # but pycha wants to iterate over ints so we do the casting ourselves
    rows = tuple(map(lambda r:
                     (int(r[0]), int(r[1])),
                     rows))

    # pycha datasets should look like this:
    # (('dataSet 1', ((0, 1), (1, 3), (2, 2.5))))
    dataset = tuple([tuple(['impresii', rows])])

    options = {
        'shouldFill': False,
        'colorScheme': {
            'args': {
                'initialColor': '#246673',
                },
            },
        'axis': {
            'labelFontSize':13,
            'tickFontSize':11,
            'tickSize':6.0,
            'x': {
                'ticks': ticks,
                'label' : 'Ziua lunii',
                },
            'y': {
                'label' : 'Impresii',
                'tickPrecision':0,
                }
            },
        'stroke': {
            'width':3,
            },
        'background' : {
            'chartColor': '#ffffff',
            'lineColor': '#FFE3EB',
            },
        'padding' : {
            'left': 70,
            'bottom': 70,
            },
        'legend' : {
            'hide': True,
            },

        }
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 300)
    chart = pycha.line.LineChart(surface, options)
    chart.addDataset(dataset)
    chart.render()

    try:
        surface.write_to_png('%sgraphs/%s.png' %
                         (settings.MEDIA_ROOT, publisher.slug))
        return '%sgraphs/%s.png' % (settings.MEDIA_URL, publisher.slug)
    except:
        return '%sgraphs/empty.png' % settings.MEDIA_URL

