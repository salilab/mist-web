from flask import request
import os
import saliweb.frontend


def handle_new_job():
    user_name = request.form.get("name", "")
    email = request.form.get("email")
    running_mode = request.form.get("running_mode")
    filtering_mode = request.form.get("filtering_mode")
    input_file = request.files.get("input_file")

    saliweb.frontend.check_email(email, required=False)
    if not input_file:
        raise saliweb.frontend.InputValidationError(
            "Please upload input table.")
    check_enum(running_mode, 'running mode', ('training', 'trained'))
    check_enum(filtering_mode, 'filtering mode', ('filtering', 'no_filtering'))

    job = saliweb.frontend.IncomingJob(user_name)

    with open(job.get_path('param.txt'), 'w') as fh:
        fh.write(running_mode + '\n')
        fh.write(filtering_mode + '\n')

    # write the input
    full_fname = job.get_path('input.txt')
    input_file.save(full_fname)
    if os.stat(full_fname).st_size == 0:
        raise saliweb.frontend.InputValidationError(
            "You have uploaded an empty input table.")

    job.submit(email)

    # Pop up an exit page
    return saliweb.frontend.render_submit_template('submit.html', job=job,
                                                   email=email)


def check_enum(value, name, options):
    """Check that enumeration `value` (with human-readable `name`) is one of
       `options`"""
    if value not in options:
        raise saliweb.frontend.InputValidationError(
            "Invalid value '%s' for %s; should be one of %s."
            % (value, name, ", ".join(repr(o) for o in options)))
