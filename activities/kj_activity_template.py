#!/usr/bin/env python3

"""
Instructions

#poopoo

- Functions intended to run for each scan
  need to be named run_xxxxx

- Do not modify the parameters of the run_xxx function
  unless you know what you are doing
  see optional parameters:
  https://github.com/tangible-landscape/grass-tangible-landscape/wiki/Running-analyses-and-developing-workflows#python-workflows

- All gs.run_command/read_command/write_command/parse_command
  need to be passed env parameter (..., env=env)
"""

import grass.script as gs


def run_slope(scanned_elev, env, **kwargs):
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', env=env)

#fun comment

def run_contours(scanned_elev, env, **kwargs):
    interval = 5
    gs.run_command('r.contour', input=scanned_elev, output='contours', step=interval, flags='t', env=env)

def run_LCP(scanned_elev, env, points=None, **kwargs):
    if not points:
        points = 'points'
        import analyses
        analyses.change_detection('scan_saved', scanned_elev, points,
                                  height_threshold=[10, 100], cells_threshold=[5, 50],
                                  add=True, max_detected=5, debug=True, env=env)
    # read coordinates into a list
    point_list = []
    data = gs.read_command('v.out.ascii', input=points, type='point',
                           format='point', separator='comma', env=env).strip().splitlines()
    for point in data:
        if point:
            point_list.append([float(p) for p in point.split(',')[:2]])
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', env=env)
    start_coordinate = point_list[0]
    end_coordinate = point_list[1]
    gs.run_command('r.cost', input='slope', output='cost', start_coordinates=start_coordinate,
                   outdir='outdir', flags='k', env=env)
    gs.run_command('r.colors', map='cost', color='gyr', env=env)
    gs.run_command('r.drain', input='cost', output='drain', direction='outdir',
                   drain='drain', flags='d', start_coordinates=end_coordinate, env=env)


def run_function_with_points(scanned_elev, env, points=None, **kwargs):
    if not points:
        points = 'points'
        import analyses
        analyses.change_detection('scan_saved', scanned_elev, points,
                                  height_threshold=[10, 100], cells_threshold=[5, 50],
                                  add=True, max_detected=5, debug=True, env=env)
    # read coordinates into a list
    point_list = []
    data = gs.read_command('v.out.ascii', input=points, type='point',
                           format='point', separator='comma', env=env).strip().splitlines()
    for point in data:
        point_list.append([float(p) for p in point.split(',')])


# this part is for testing without TL
def main():
    import os

    # we want to run this repetetively without deleted the created files
    os.environ['GRASS_OVERWRITE'] = '1'

    elevation = 'elev_lid792_1m'
    elev_resampled = 'elev_resampled'
    # resampling to have similar resolution as with TL
    gs.run_command('g.region', raster=elevation, res=4, flags='a')
    gs.run_command('r.resamp.stats', input=elevation, output=elev_resampled)

    # create points
    points = 'points'
    gs.write_command('v.in.ascii', flags='t', input='-', output=points, separator='comma',
                     stdin='638432,220382\n638621,220607')
    print("Hello!")
    LCP(scanned_elev=elev_resampled, env=None, points=points)


    # create points
    points = 'points'
    gs.write_command('v.in.ascii', flags='t', input='-', output=points, separator='comma',
                     stdin='638432,220382\n638621,220607')
    print("Hiya!")
    run_LCP(scanned_elev=elev_resampled, env=None, points=points)



if __name__ == '__main__':
    main()

