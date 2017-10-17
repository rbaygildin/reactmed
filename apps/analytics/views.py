import base64
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pandas import ExcelWriter

import apps.analytics.visualizers as vis
from apps.analytics.analysis import FeaturesSelectionAnalyser, ImputerAnalyser, DescriptiveStatAnalyser
from apps.analytics.etl import PostgresDataLoader
from apps.analytics.load import data_load
from apps.core.models import Patient

PostgresDataLoader.configure_data_source(
    dbname='laksmimed_db',
    user='laksmimed_user',
    password='laksmimed95root',
)


def visualize_action(request):
    """
    This view returns visual representation of
    datasets
    """
    try:
        test = request.GET.get('test')
        class_col = request.GET.get('class_col')
        feature_cols = request.GET.getlist('feature_cols[]', None)
        vis_method = request.GET.get("vis_method")
        alpha = request.GET.get('alpha', 1.0)
        width = request.GET.get('width', 8)
        height = request.GET.get('height', 8)
        color_map = request.GET.get('color_map', 'brg')
        out_view = request.GET.get('out_view')
        n_features = request.GET.get('n_features', 0)
        select_method = request.GET.get('select_method', 'none')
        patients = request.GET.getlist('patients[]', None)

        if test is None or test == '':
            raise ValueError('Медицинское обследование должно быть задано!')
        if class_col is None or class_col == '':
            raise ValueError('Класс-колонка должна быть задана!')
        if vis_method is None or vis_method == '':
            raise ValueError('Метод визуализации должен быть задан!')
        print("Patients")
        print(patients)

        if patients is not None and len(patients) == 0:
            patients = None

        if patients is not None:
            patients = Patient.objects.filter(pk__in=map(lambda p: int(p), patients))
            patients_temp = {}
            for p in patients:
                patients_temp[p.id] = {
                    'full_name': p.full_name
                }
            patients = patients_temp

        df, class_col = data_load(test=test, class_col=class_col, feature_cols=feature_cols, load_pattern='fc',
                                  normalize="std")

        limit = request.GET.get('limit')
        offset = request.GET.get('offset')

        if (limit is not None and limit.isdigit()) and (offset is not None and offset.isdigit()):
            limit = int(limit) - 1
            offset = int(offset)
            df = df.ix[offset:limit]

        out_format = request.GET.get("format")
        response = HttpResponse()
        out = None

        if out_view == 'bin':
            out = response
            if out_format == "svg":
                response['Content-Type'] = 'image/svg+xml'
            elif out_format == "png":
                response['Content-Type'] = 'image/img'
        elif out_view == 'base64':
            out = BytesIO()

        df = ImputerAnalyser().perform_analysis(df=df, class_col=class_col)

        if select_method != 'none':
            selector = FeaturesSelectionAnalyser()
            df = selector.perform_analysis(df, class_col=class_col, select_method=select_method, n_features=n_features)

        kwargs = {
            "alpha": float(alpha),
            "color_map": color_map,
            "class_col": class_col,
            "out": out,
            "format": out_format,
            "patients": patients,
            "width": int(width),
            "height": int(height)
        }

        if vis_method.lower() == "andrews_curves":
            visualizer = vis.AndrewsCurvesVisualizer(**kwargs)
        elif vis_method.lower() == "pca":
            visualizer = vis.PCAVisualizer(**kwargs)
        elif vis_method.lower() == "parallel_coords":
            visualizer = vis.ParallelCoordinatesVisualizer(**kwargs)
        elif vis_method.lower() == "radviz":
            visualizer = vis.RadVizVisualizer(**kwargs)
        elif vis_method.lower() == "hist":
            visualizer = vis.HistVisualizer(**kwargs)
        elif vis_method.lower() == "corrmatrix":
            visualizer = vis.CorrHeatMapVisualizer(**kwargs)
        elif vis_method.lower() == "dist":
            kwargs["bins"] = int(request.GET.get('bins'))
            visualizer = vis.DistVisualizer(**kwargs)
        elif vis_method.lower() == "boxplot":
            visualizer = vis.BoxplotVisualizer(**kwargs)
        elif vis_method.lower() == "pairwise":
            kwargs["reg_type"] = request.GET.get('reg_type')
            # kwargs["degree"] = int(request.args.get('degree'))
            # kwargs["bins"] = int(request.args.get('bins'))
            visualizer = vis.PairWiseVisualizer(**kwargs)
        visualizer.visualize(df)
        if out_view == 'base64':
            response = HttpResponse(base64.b64encode(out.getvalue()))
        return response
    except Exception as e:
        print(e)
        error_message = {
            "message": str(e)
        }
        return JsonResponse(status=500, data=error_message)


def cluster_action(request):
    cluster_method = request.GET.get("cluster_method")
    test = request.GET.get('test')
    feature_cols = request.GET.get('feature_cols')
    n_features = int(request.GET.get('n_features') or 0)
    select_method = request.GET.get('select_method', 'none')
    res = data_load(test=test, feature_cols=feature_cols, load_pattern='f', normalize="std")
    df = res[0]
    out_format = request.GET.get("format")
    out_view = request.GET.get('out_view')
    alpha = request.GET.get("alpha")
    alpha = float(alpha) if not (alpha is None or alpha == "") else 1.0
    color_map = request.GET.get('color_map')
    width = request.GET.get('width')
    height = request.GET.get('height')
    width = int(width) if not (width is None or width == "") else 8
    height = int(height) if not (height is None or height == "") else 8
    perf_method = request.GET.get("perf_method")
    n_clusters = request.GET.getlist("n_clusters[]")
    patients = request.GET.getlist('patients[]', None)
    print(patients)

    if patients is not None and len(patients) > 0:
        patients = PostgresDataLoader().load_data(
            query="SELECT patient_id, last_name || ' ' || first_name AS full_name "
                  "FROM patients "
                  "WHERE patient_id in (%s)" % " ,".join(patients))
    else:
        patients = None

    if select_method != 'none':
        selector = FeaturesSelectionAnalyser()
        df = selector.perform_analysis(df, select_method=select_method, n_features=n_features)
    df = ImputerAnalyser().perform_analysis(df=df)

    visualizer = None
    response = HttpResponse()
    out = None

    if out_view == 'bin':
        out = response
        if out_format == "svg":
            response['Content-Type'] = 'image/svg+xml'
        elif out_format == "png":
            response['Content-Type'] = 'image/img'
    elif out_view == 'base64':
        out = BytesIO()

    kwargs = {
        "out": out,
        "alpha": float(alpha),
        "color_map": color_map,
        "width": width,
        "height": height,
        "perf_method": perf_method,
        "format": out_format,
        "n_clusters": n_clusters,
        "patients": patients
    }

    if cluster_method == "k_means":
        visualizer = vis.KMeansClusteringVisualizer(**kwargs)
    elif cluster_method == "mini_batch_k_means":
        visualizer = vis.MiniBatchKMeansClusteringVisualizer(**kwargs)
    elif cluster_method == "agglomerative":
        linkage = request.GET.get('linkage')
        kwargs["linkage"] = linkage
        visualizer = vis.AgglomerativeClusteringVisualizer(**kwargs)
    elif cluster_method == "mean_shift":
        quantile = float(request.GET.get('quantile') or 0.3)
        kwargs["quantile"] = quantile
        visualizer = vis.MeanShiftClusteringVisualizer(**kwargs)
    visualizer.visualize(df)
    if out_view == 'base64':
        response = HttpResponse(base64.b64encode(out.getvalue()))
    return response


def data_action(request):
    out_format = request.GET.get("format")
    select_method = request.GET.get('select_method')
    n_features = int(request.GET.get('n_features') or 0)
    kwargs = {
        'test': request.GET.get('test'),
        'feature_cols': request.GET.getlist('feature_cols'),
        'class_col': request.GET.get('class_col'),
        'normalize': request.GET.get('normalize'),
        'load_pattern': request.GET.get('load_pattern')
    }
    df, class_col = data_load(**kwargs)
    print(class_col)
    if select_method != 'none':
        selector = FeaturesSelectionAnalyser()
        if class_col is None:
            df = selector.perform_analysis(df, select_method=select_method, n_features=n_features)
        else:
            df = selector.perform_analysis(df, class_col=class_col, select_method=select_method, n_features=n_features)
    if class_col is None:
        df = ImputerAnalyser().perform_analysis(df=df)
    else:
        df = ImputerAnalyser().perform_analysis(df=df, class_col=class_col)
    df.reset_index(level=0, inplace=True)
    orient = request.GET.get("orient")
    if out_format == 'application/json':
        return HttpResponse(df.reset_index().to_json(orient=orient), content_type=out_format)
    elif out_format == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        sio = BytesIO()
        writer = ExcelWriter('data.xlsx', engine='xlsxwriter')
        writer.book.filename = sio
        df.reset_index().to_excel(excel_writer=writer)
        writer.save()
        sio.seek(0)
        file = sio.getvalue()
        response = HttpResponse(file, content_type=out_format)
        response['Content-Disposition'] = 'attachment; filename=data.xlsx'
        return response
    elif out_format == 'text/html':
        return HttpResponse(df.reset_index().to_html(), content_type=out_format)
    return HttpResponse(df.reset_index().to_csv(), content_type='text/csv')


def features_stat_action(request):
    kwargs = {
        'test': request.GET.get('test'),
        'feature_cols': request.GET.getlist('feature_cols'),
        'class_col': request.GET.get('class_col'),
        'normalize': request.GET.get('normalize'),
        'load_pattern': request.GET.get('load_pattern')
    }
    df, class_col = data_load(**kwargs)
    stat = DescriptiveStatAnalyser().perform_analysis(df, class_col=class_col)
    orient = request.GET.get("orient")
    return HttpResponse(stat.to_json(orient=orient), content_type='application/json')


@login_required
def datasets_page_action(request):
    patients = request.user.patients.all()
    return render(request, 'analytics/data_sets.html', {'patients': patients})


@login_required
def visualize_page_action(request):
    patients = request.user.patients.all()
    return render(request, 'analytics/visualization.html', {'patients': patients})


@login_required
def clustering_page_action(request):
    patients = request.user.patients.all()
    return render(request, 'analytics/clustering.html', {'patients': patients})
