from flask import render_template, request, redirect, url_for

def advanced_search_form():
    return render_template("advanced_search.html")

def search_advanced():
    form = request.form
    filters = {
        'budget_min': form.get('budget_range_min', type=int),
        'budget_max': form.get('budget_range_max', type=int),
        'cpu_min': form.get('cpu_range_min', type=int),
        'cpu_max': form.get('cpu_range_max', type=int),
        'gpu_min': form.get('gpu_range_min', type=int),
        'gpu_max': form.get('gpu_range_max', type=int),
        'display_min': form.get('display_range_min', type=float),
        'display_max': form.get('display_range_max', type=float),
        'ram_options': request.form.getlist('ram'),
        'storage_options': request.form.getlist('storage'),
        'resolution_options': request.form.getlist('resolution'),
        'port_hdmi': form.get('port_hdmi'),
        'port_sd': form.get('port_sd'),
        'port_lan': form.get('port_lan'),
        'pd_charge': form.get('pd_charge'),
        'thunderbolt': form.get('thunderbolt'),
    }
    return redirect(url_for("render_results", **filters))
