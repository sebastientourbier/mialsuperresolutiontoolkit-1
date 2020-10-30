#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json
# from traits.api import *

# Import the super-resolution pipeline
from pymialsrtk.parser import get_parser
from pymialsrtk.pipelines.anatomical.srr import AnatomicalPipeline


def main(bids_dir, output_dir, subject, p_stacksOrder, session, paramTV=dict(), number_of_cores=1, srID=None, use_manual_masks=False):

    subject = 'sub-' + subject
    if session is not None:
        session = 'ses-' + session

    if srID is None:
        srID = "01"

    # Initialize an instance of AnatomicalPipeline
    pipeline = AnatomicalPipeline(bids_dir,
                                  output_dir,
                                  subject,
                                  p_stacksOrder,
                                  srID,
                                  session,
                                  paramTV,
                                  use_manual_masks)
    # Create the super resolution Nipype workflow
    pipeline.create_workflow()

    # Execute the workflow
    res = pipeline.run(number_of_cores)

    return res


if __name__ == '__main__':

    bids_dir = os.path.join('/fetaldata')

    parser = get_parser()
    args = parser.parse_args()

    print(args.param_file)
    with open(args.param_file, 'r') as f:
        participants_params = json.load(f)
        print(participants_params)
        print(participants_params.keys())
    print()

    if len(args.participant_label) >= 1:
        for sub in args.participant_label:

            if sub in participants_params.keys():
                sr_list = participants_params[sub]
                print(sr_list)

                for iSr, sr_params in enumerate(sr_list):

                    ses = sr_params["session"] if "session" in sr_params.keys() else None

                    print('sr_params')
                    if ("stacksOrder" not in sr_params.keys()) or ("sr-id" not in sr_params.keys()):
                        print('Do not process subjects %s because of missing parameters.' % sub)
                        continue

                    if 'paramTV' in sr_params.keys():

                        res = main(bids_dir=args.bids_dir,
                                   output_dir=args.output_dir,
                                   subject=sub,
                                   p_stacksOrder=sr_params['stacksOrder'],
                                   session=ses,
                                   paramTV=sr_params['paramTV'],
                                   srID=sr_params['sr-id'],
                                   use_manual_masks=args.manual)

                        # sys.exit(0)

                    else:

                        res = main(bids_dir=args.bids_dir,
                                   output_dir=args.output_dir,
                                   subject=sub,
                                   p_stacksOrder=sr_params['stacksOrder'],
                                   session=ses,
                                   srID=sr_params['sr-id'],
                                   use_manual_masks=args.manual)

                        # sys.exit(0)
    else:
        print('ERROR: Processing of all dataset not implemented yet\n At least one participant label should be provided')
        sys.exit(2)