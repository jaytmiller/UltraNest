import os
import sys
import argparse
import numpy as np
from numpy import cos, pi

def main(args):

    def loglike(z):
        chi = (cos(z / 2.)).prod(axis=1)
        return (2. + chi)**5

    def transform(x):
        return x * 10 * pi
    
    import string
    paramnames = list(string.ascii_lowercase)[:args.x_dim]
    
    if args.reactive:
        from mininest import ReactiveNestedSampler
        sampler = ReactiveNestedSampler(paramnames, loglike, transform=transform, 
            log_dir=args.log_dir, append_run_num=False,
            draw_multiple=False,
        )
        sampler.run(log_interval=20, 
            max_num_improvement_loops=10, min_num_live_points=args.num_live_points,)
        sampler.print_results()
        sampler.plot()
    else:
        from mininest import NestedSampler
        sampler = NestedSampler(paramnames, loglike, transform=transform, 
            num_live_points=args.num_live_points,
            log_dir=args.log_dir, append_run_num=True)
            #log_dir=None)
        sampler.run(log_interval=20)
        sampler.print_results()
        sampler.plot()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--x_dim', type=int, default=2,
                        help="Dimensionality")
    parser.add_argument("--num_live_points", type=int, default=1000)
    parser.add_argument('--noise', type=float, default=-1)
    parser.add_argument('--log_dir', type=str, default='logs/eggbox')
    parser.add_argument('--reactive', action='store_true')

    args = parser.parse_args()
    main(args)
