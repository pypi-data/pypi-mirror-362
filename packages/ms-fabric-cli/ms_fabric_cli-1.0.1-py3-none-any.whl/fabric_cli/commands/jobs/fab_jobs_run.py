# Copyright (c) Microsoft Corporation.
# Licensed under the EULA license.

import json
from argparse import Namespace

from fabric_cli.client import fab_api_jobs as jobs_api
from fabric_cli.core import fab_constant as con
from fabric_cli.core import fab_state_config as config
from fabric_cli.core.hiearchy.fab_hiearchy import Item
from fabric_cli.utils import fab_cmd_job_utils as utils_job
from fabric_cli.utils import fab_ui as utils_ui


def exec_command(args: Namespace, item: Item) -> None:
    if getattr(args, "configuration", None) is not None:
        payload = json.dumps({"executionData": json.loads(args.configuration)})
    else:
        payload = None

    (response, job_instance_id) = jobs_api.run_on_demand_item_job(args, payload)

    if response.status_code == 202:
        if args.wait:
            utils_ui.print_grey(f"∟ Job instance '{job_instance_id}' created")
            # retry_after = int(response.headers.get("Retry-After"))
            timeout = getattr(args, "timeout", None)
            if timeout is not None:
                utils_ui.print_grey(f"∟ Timeout: {timeout} seconds")
            else:
                utils_ui.print_grey("∟ Timeout: no timeout specified")

            try:
                utils_job.wait_for_job_completion(
                    args.ws_id,
                    args.item_id,
                    job_instance_id,
                    timeout=timeout,
                )
            except TimeoutError as e:
                utils_ui.print_warning(str(e))
                # Get the configuration to check if we should cancel the job
                if config.get_config(con.FAB_JOB_CANCEL_ONTIMEOUT) == "false":
                    utils_ui.print_grey(
                        f"Job still running. To change this behaviour and cancel on timeout, set {con.FAB_JOB_CANCEL_ONTIMEOUT} config property to 'true'"
                    )
                else:
                    utils_ui.print_grey(
                        f"Cancelling job instance '{job_instance_id}' (timeout). To change this behaviour and continue running on timeout, set {con.FAB_JOB_CANCEL_ONTIMEOUT} config property to 'false'"
                    )
                    args.instance_id = job_instance_id
                    response = jobs_api.cancel_item_job_instance(args)
                    if response.status_code == 202:
                        utils_ui.print_done(
                            f"Job instance '{args.instance_id}' cancelled (async)"
                        )

        else:
            utils_ui.print_done(f"Job instance '{job_instance_id}' created")
            utils_ui.print_grey(
                f"→ To see status run 'job run-status {item.path} --id {job_instance_id}'"
            )
