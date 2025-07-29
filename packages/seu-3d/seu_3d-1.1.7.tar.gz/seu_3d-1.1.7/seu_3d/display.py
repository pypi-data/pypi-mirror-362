import os
os.environ["QT_ENABLE_GLYPH_CACHE_SHARING"] = "1"
from qtpy import QtCore, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
from qtpy.QtWidgets import QTabWidget, QVBoxLayout, QWidget
from magicgui import widgets
from ._umap_selection import UmapSelection
from ._utils import error_points_selection, safe_toarray
from napari.utils.colormaps import ALL_COLORMAPS, Colormap
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib import cm, colors
import numpy as np
import logging
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy as sch
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import colorcet as cc
import scanpy as sc
import squidpy as sq
from tqdm import tqdm
import sys
from scipy.sparse import issparse
try:
    from pyvista import PolyData

    pyvista = True
except Exception as e:
    print(
        (
            "pyvista is not installed. No surfaces can be generated\n"
            "Try pip install pyvista or conda install pyvista to install it"
        )
    )
    pyvista = False

class DisplayEmbryo():
    '''
    Class to display and analyse the Embryo data in a napari viewer.
    '''
    def color_set(self):
        tissue_color_map = {
            'Epiblast': [0.38823529411764707, 0.3333333333333333, 0.2784313725490196],
            'Primitive streak': [0.8549019607843137, 0.7450980392156863, 0.6],
            'ExE ectoderm': [0.596078431372549, 0.596078431372549, 0.596078431372549],
            'Visceral endoderm': [0.9647058823529412, 0.7490196078431373, 0.796078431372549],
            'ExE endoderm': [0.4980392156862745, 0.40784313725490196, 0.4549019607843137],
            'Nascent mesoderm': [0.7725490196078432, 0.5803921568627451, 0.7490196078431373],
            'Rostral neurectoderm': [0.396078431372549, 0.6588235294117647, 0.24313725490196078],
            'Blood progenitors 2': [0.788235294117647, 0.6627450980392157, 0.592156862745098],
            'Mixed mesoderm': [0.8745098039215686, 0.803921568627451, 0.8941176470588236],
            'ExE mesoderm': [0.5333333333333333, 0.4392156862745098, 0.6784313725490196],
            'Intermediate mesoderm': [0.07450980392156863, 0.6, 0.5725490196078431],
            'Pharyngeal mesoderm': [0.788235294117647, 0.9215686274509803, 0.984313725490196],
            'Caudal epiblast': [0.6196078431372549, 0.403921568627451, 0.3843137254901961],
            'PGC': [0.9803921568627451, 0.796078431372549, 0.07058823529411765],
            'Mesenchyme': [0.8, 0.47058823529411764, 0.09411764705882353],
            'Haematoendothelial progenitors': [0.984313725490196, 0.7450980392156863, 0.5725490196078431],
            'Blood progenitors 1': [0.9764705882352941, 0.8705882352941177, 0.8117647058823529],
            'Surface ectoderm': [0.9686274509803922, 0.9686274509803922, 0.6196078431372549],
            'Gut': [0.9372549019607843, 0.35294117647058826, 0.615686274509804],
            'Paraxial mesoderm': [0.5529411764705883, 0.7098039215686275, 0.807843137254902],
            'Caudal neurectoderm': [0.20784313725490197, 0.3058823529411765, 0.13725490196078433],
            'Notochord': [0.058823529411764705, 0.2901960784313726, 0.611764705882353],
            'Pre-somitic' : [0.0, 0.3333333333333333, 0.4745098039215686],
            'pre-somitic':[0.0, 0.3333333333333333, 0.4745098039215686],
            'Somitic mesoderm':[0.0, 0.3333333333333333, 0.4745098039215686],
            'Somitic Esoderm': [0.0, 0.3333333333333333, 0.4745098039215686],
            'Caudal Mesoderm': [0.24705882352941178, 0.5176470588235295, 0.6666666666666666],
            'Erythroid1': [0.7803921568627451, 0.13333333333333333, 0.1568627450980392],
            'Def. endoderm': [0.9529411764705882, 0.592156862745098, 0.7529411764705882],
            'Parietal endoderm': [0.10196078431372549, 0.10196078431372549, 0.10196078431372549],
            'Allantois': [0.3254901960784314, 0.17254901960784313, 0.5411764705882353],
            'Anterior primitive Streak': [0.7568627450980392, 0.6235294117647059, 0.4392156862745098],
            'Endothelium': [1.0, 0.5372549019607843, 0.10980392156862745],
            'Forebrain/Midbrain/Hindbrain': [0.39215686274509803, 0.47843137254901963, 0.30980392156862746],
            'Spinal cord': [0.803921568627451, 0.8784313725490196, 0.5333333333333333],
            'Cardiomyocytes': [0.7098039215686275, 0.11372549019607843, 0.5529411764705883],
            'Erythroid2': [0.9686274509803922, 0.5647058823529412, 0.5137254901960784],
            'NMP': [0.5568627450980392, 0.7803921568627451, 0.5725490196078431],
            'Erythroid 3': [0.9372549019607843, 0.3058823529411765, 0.13333333333333333],
            'Neural crest': [0.7647058823529411, 0.7647058823529411, 0.5333333333333333],
        }
        extra_colors = [[0.12549019607843137, 0.27450980392156865, 0.8392156862745098],
                        [0.9137254901960784, 0.43529411764705883, 0.28627450980392155],
                        [0.3843137254901961, 0.8431372549019608, 0.5372549019607843],
                        [0.6196078431372549, 0.09803921568627451, 0.8196078431372549],
                        [0.20784313725490197, 0.8470588235294118, 0.9450980392156862],
                        [0.9333333333333333, 0.27450980392156865, 0.8509803921568627],
                        [0.5490196078431373, 0.803921568627451, 0.1607843137254902],
                        [0.8392156862745098, 0.09411764705882353, 0.6274509803921569],
                        [0.1568627450980392, 0.5764705882352941, 0.3411764705882353],
                        [0.8392156862745098, 0.48627450980392156, 0.08235294117647059],
                        [0.43529411764705883, 0.25098039215686274, 0.9176470588235294],
                        [0.9764705882352941, 0.6431372549019608, 0.1568627450980392],
                        [0.30980392156862746, 0.6745098039215687, 0.8274509803921568],
                        [0.7529411764705882, 0.06666666666666667, 0.3843137254901961],
                        [0.12549019607843137, 0.8392156862745098, 0.7411764705882353],
                        [0.9058823529411765, 0.20784313725490197, 0.13725490196078433],
                        [0.3607843137254902, 0.1411764705882353, 0.9098039215686274],
                        [0.8431372549019608, 0.396078431372549, 0.6627450980392157],
                        [0.21568627450980393, 0.8784313725490196, 0.23921568627450981],
                        [0.9333333333333333, 0.14901960784313725, 0.7568627450980392],
                        [0.4666666666666667, 0.7607843137254902, 0.13725490196078433],
                        [0.9137254901960784, 0.3215686274509804, 0.6745098039215687],
                        [0.30980392156862746, 0.8588235294117647, 0.9764705882352941],
                        [0.8156862745098039, 0.09019607843137255, 0.4980392156862745],
                        [0.5843137254901961, 0.9137254901960784, 0.2980392156862745],
                        [0.10980392156862745, 0.2823529411764706, 0.9098039215686274],
                        [0.9019607843137255, 0.49019607843137253, 0.12549019607843137],
                        [0.2784313725490196, 0.9058823529411765, 0.6627450980392157],
                        [0.7490196078431373, 0.08235294117647059, 0.2901960784313726],
                        [0.09411764705882353, 0.6274509803921569, 0.8941176470588236],
                        [0.8941176470588236, 0.33725490196078434, 0.5803921568627451],
                        [0.5372549019607843, 0.9137254901960784, 0.12941176470588237],
                        [0.2823529411764706, 0.1411764705882353, 0.9176470588235294],
                        [0.8745098039215686, 0.6392156862745098, 0.1450980392156863],
                        [0.21568627450980393, 0.8235294117647058, 0.9450980392156862],
                        [0.9176470588235294, 0.30196078431372547, 0.1568627450980392],
                        [0.48627450980392156, 0.22745098039215686, 0.8901960784313725],
                        [0.8980392156862745, 0.5137254901960784, 0.09411764705882353],
                        [0.1607843137254902, 0.6627450980392157, 0.9137254901960784],
                        [0.8784313725490196, 0.3803921568627451, 0.6509803921568628],
                        [0.6549019607843137, 0.8901960784313725, 0.1568627450980392],
                        [0.28627450980392155, 0.12549019607843137, 0.9098039215686274],
                        [0.8980392156862745, 0.6509803921568628, 0.10588235294117647],
                        [0.23921568627450981, 0.6784313725490196, 0.8549019607843137],
                        [0.8352941176470589, 0.2196078431372549, 0.1411764705882353],
                        [0.5764705882352941, 0.8549019607843137, 0.33725490196078434]]

        tissue = list(self.embryo.all_tissues)
        self.tissue_color_map = {}
        i = 0
        for tissue_name in tissue:
            if tissue_name in tissue_color_map:
                self.tissue_color_map[tissue_name] = tissue_color_map[tissue_name]
            else:
                self.tissue_color_map[tissue_name] = extra_colors[i]
                i += 1
    
    def legend_tab(self):
        '''
        Create the legend tab
        '''
        with plt.style.context('dark_background'):
            fig, ax = plt.subplots()
            ax.axis('off')

            for color,tissue in zip(self.tissue_color_map.values(), self.tissue_color_map.keys()):
                ax.plot([], [], 's', markersize=9, color=color, label=tissue)
            canvas = FigureCanvas(fig)
            legend = fig.legend(
                loc='center',
                bbox_to_anchor=(0.5,0.5),
                frameon=False,
                fontsize=9,
            )

        legend_tab = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        legend_tab.setObjectName("legend_tab")
        legend_tab.setLayout(layout)

        return legend_tab
    
    def tissue_filter(self):
        '''
        Create a tissue filter fuction
        '''
        points = self.viewer.layers.selection.active
        if points is None or points.as_layer_data_tuple()[-1] != "points":
            error_points_selection()
        adata = self.embryo.adata

        selected_tissue = self.tissue_select.value
        selected_slice = self.slice_select.value
        selected_germ_layer = self.germ_layer_select.value
        select_xyz = [[self.show_x_min.value, self.show_x_max.value],
                    [self.show_y_min.value, self.show_y_max.value],
                    [self.show_z_min.value, self.show_z_max.value]]
        
        mask = np.ones(len(adata), dtype=bool)
        mask &= adata.obs[self.embryo.tissue_name].isin(selected_tissue)

        if 'slice' in adata.obs.columns:
            mask &= adata.obs['slice'].isin(selected_slice)
        elif 'orig.ident' in adata.obs.columns:
            mask &= adata.obs['orig.ident'].isin(selected_slice)

        if 'germ_layer' in adata.obs.columns:
            mask &= adata.obs['germ_layer'].isin(selected_germ_layer)

        coords = adata.obsm[self.embryo.coordinate_3d_key]
        x_mask = (coords[:, 0] >= select_xyz[0][0]) & (coords[:, 0] <= select_xyz[0][1])
        y_mask = (coords[:, 1] >= select_xyz[1][0]) & (coords[:, 1] <= select_xyz[1][1])
        z_mask = (coords[:, 2] >= select_xyz[2][0]) & (coords[:, 2] <= select_xyz[2][1])
        mask &= x_mask & y_mask & z_mask


        self.selected_adata = adata[mask].copy()
        points.shown = mask
        self.mask_filter = mask
        points.refresh()
        
    def tissue_tab(self):
        viewer = self.viewer
        def celltype_coloring():
            points = viewer.layers.selection.active
            adata = self.embryo.adata
            tissue_types = adata.obs[self.embryo.tissue_name].astype(str).values
            self.viewer.dims.ndisplay = 3
            position = adata.obsm[self.embryo.coordinate_3d_key]
            points.features = adata.obs
            points.data = position
            points.face_color = [self.tissue_color_map[t] for t in tissue_types]
        def select_tissue():
            self.tissue_select = widgets.Select(
                choices=self.embryo.all_tissues,
                value=self.embryo.all_tissues,
            )
            run_tissue_filter = widgets.FunctionGui(
                self.tissue_filter,
                call_button="Select Tissue",
                layout="vertical",
            )
            run_celltype_coloring = widgets.FunctionGui(
                celltype_coloring,
                call_button="Color by Tissue",
                layout="vertical",
            )
            run_show_flatten = widgets.FunctionGui(
                self.show_flatten,
                call_button="Show in Flatten",
                layout="vertical",
            )
            select_tissue_container = widgets.Container(
                widgets=[self.tissue_select, run_tissue_filter,run_celltype_coloring, run_show_flatten],
                layout="vertical",
            )
            return select_tissue_container
        
        tissue_tab = QTabWidget()
        tissue_tab.setObjectName("Tissue")
        tissue_tab.addTab(select_tissue().native, "Select Tissue")

        return tissue_tab
    
    def show_flatten(self):
        adata = self.embryo.adata
        points = self.viewer.layers.selection.active
        if points is None or points.as_layer_data_tuple()[-1] != "points":
            error_points_selection(show=True)
            return
        if 'x_flatten' not in adata.obs.columns or 'y_flatten' not in adata.obs.columns:
            logging.warning(
                "x_flatten and y_flatten columns not found in adata.obs. "
            )
            return
        else:
            x_flatten = adata.obs['y_flatten'].values
            y_flatten = adata.obs['x_flatten'].values
            xy_flatten = np.column_stack((x_flatten, y_flatten))
        shown_ori = points.shown
        colors = points.face_color
        self.viewer.add_points(
            xy_flatten,
            size=10,
            face_color=colors,
            features=adata.obs,
            name='flatten',
            shown=shown_ori,
        )

    def slice_tab(self):
        def select_slice():
            if 'slices' in self.embryo.adata.obs.columns:
                self.slice_select = widgets.Select(
                    choices=self.embryo.adata.obs['slices'].unique().tolist(),
                    value=self.embryo.adata.obs['slices'].unique().tolist(),
                )
            elif 'orig.ident' in self.embryo.adata.obs.columns:
                self.slice_select = widgets.Select(
                    choices=self.embryo.adata.obs['orig.ident'].unique().tolist(),
                    value=self.embryo.adata.obs['orig.ident'].unique().tolist(),
                )
            else:
                self.slice_select = widgets.Select(
                    choices=["No slice available"],
                    value="No slice available",
                    enabled=False,
                )
            run_slice_filter = widgets.FunctionGui(
                self.tissue_filter,
                call_button="Select Slice",
                layout="vertical",
            )
            select_slice_container = widgets.Container(
                widgets=[self.slice_select, run_slice_filter],
                layout="vertical",
            )
            return select_slice_container

        slice_tab = QTabWidget()
        slice_tab.setObjectName("Slice")
        slice_tab.addTab(select_slice().native, "Select Slice")

        return slice_tab
    
    def germ_layer_tab(self):
        def select_germ_layer():
            if 'germ_layer' in self.embryo.adata.obs.columns:
                self.germ_layer_select = widgets.Select(
                    choices=self.embryo.adata.obs['germ_layer'].unique().tolist(),
                    value=self.embryo.adata.obs['germ_layer'].unique().tolist(),
                )
            else:
                self.germ_layer_select = widgets.Select(
                    choices=["No slice available"],
                    value="No slice available",
                    enabled=False,
                )
            run_germ_layer_filter = widgets.FunctionGui(
                self.tissue_filter,
                call_button="Select Germ Layer",
                layout="vertical",
            )
            select_germ_layer_container = widgets.Container(
                widgets=[self.germ_layer_select, run_germ_layer_filter],
                layout="vertical",
            )
            return select_germ_layer_container

        germ_layer_tab = QTabWidget()
        germ_layer_tab.setObjectName("Germ Layer")
        germ_layer_tab.addTab(select_germ_layer().native, "Select Germ Layer")

        return germ_layer_tab
    
    def selectXY_tab(self):
        coordinate_3d = self.embryo.coordinate_3d
        x_min, x_max = coordinate_3d[:, 0].min(), coordinate_3d[:, 0].max()
        y_min, y_max = coordinate_3d[:, 1].min(), coordinate_3d[:, 1].max()
        z_min, z_max = coordinate_3d[:, 2].min(), coordinate_3d[:, 2].max()
        def tissue_filter_preview():
            x_min = self.show_x_min.value
            x_max = self.show_x_max.value
            y_min = self.show_y_min.value
            y_max = self.show_y_max.value
            z_min = self.show_z_min.value
            z_max = self.show_z_max.value
            vertices = np.array([
                [x_min, y_min, z_min],
                [x_max, y_min, z_min],
                [x_max, y_max, z_min],
                [x_min, y_max, z_min],
                [x_min, y_min, z_max],
                [x_max, y_min, z_max],
                [x_max, y_max, z_max],
                [x_min, y_max, z_max]
            ])
            faces = np.array([
                [0, 1, 2], [0, 2, 3],
                [4, 5, 6], [4, 6, 7],
                [0, 1, 5], [0, 5, 4],
                [3, 2, 6], [3, 6, 7],
                [0, 3, 7], [0, 7, 4],
                [1, 2, 6], [1, 6, 5]
            ])
            self.viewer.add_surface(
                (vertices, faces),
                colormap='gray',
                opacity=0.5,
                shading='flat',
                name = 'preview_box',
            )
        def select_xyz():
            self.show_x_min = widgets.FloatSpinBox(
                value=x_min, min=x_min - (abs(x_min) * 0.9), max=x_max * 1.1, step=0.1, label="X Min"
            )
            self.show_x_max = widgets.FloatSpinBox(
                value=x_max, min=x_min - (abs(x_min) * 0.9), max=x_max * 1.1, step=0.1, label="X Max"
            )
            self.show_y_min = widgets.FloatSpinBox(
                value=y_min, min=y_min - (abs(y_min) * 0.9), max=y_max * 1.1, step=0.1, label="Y Min"
            )
            self.show_y_max = widgets.FloatSpinBox(
                value=y_max, min=y_min - (abs(y_min) * 0.9), max=y_max * 1.1, step=0.1, label="Y Max"
            )
            self.show_z_min = widgets.FloatSpinBox(
                value=z_min, min=z_min - (abs(z_min) * 0.9), max=z_max * 1.1, step=0.1, label="Z Min"
            )
            self.show_z_max = widgets.FloatSpinBox(
                value=z_max, min=z_min - (abs(z_min) * 0.9), max=z_max * 1.1, step=0.1, label="Z Max"
            )
            run_xy_filter_preview = widgets.FunctionGui(
                tissue_filter_preview,
                call_button="Preview select XYZ",
                layout="vertical",
            )
            run_xy_filter = widgets.FunctionGui(
                self.tissue_filter,
                call_button="Select XYZ",
                layout="vertical",
            )
            note = widgets.Label(value="Note!Remenber select point layer after preview!")
            select_xyz_container = widgets.Container(
                widgets=[
                    self.show_x_min,
                    self.show_x_max,
                    self.show_y_min,
                    self.show_y_max,
                    self.show_z_min,
                    self.show_z_max,
                    run_xy_filter_preview,
                    run_xy_filter,
                    note
                ],
                layout="vertical",
            )
            return select_xyz_container
        
        selectXY_tab = QTabWidget()
        selectXY_tab.addTab(select_xyz().native, "Select XYZ")

        return selectXY_tab
    
    def surface_tab(self):
        def show_surf():
            surf_tissue = self.surf_tissue.value
            adata = self.embryo.adata.copy()
            adata_surf = adata[adata.obs[self.embryo.tissue_name].isin(surf_tissue)]
            points = adata_surf.obsm[self.embryo.coordinate_3d_key]
            pd = PolyData(points)
            mesh = pd.delaunay_3d().extract_surface()
            face_list = list(mesh.faces.copy())
            face_sizes = {}
            faces = []
            while 0 < len(face_list):
                nb_P = face_list.pop(0)
                if not nb_P in face_sizes:
                    face_sizes[nb_P] = 0
                face_sizes[nb_P] += 1
                curr_face = []
                for _ in range(nb_P):
                    curr_face.append(face_list.pop(0))
                faces.append(curr_face)
            faces = np.array(faces)
            self.viewer.add_surface(
                (mesh.points, faces),
                colormap=self.tissue_color_map[surf_tissue[0]],
                opacity=0.5,
                name = 'surface_' + surf_tissue[0],
            )
        def select_surf():
            if pyvista:
                surf_label = widgets.Label(value="Choose tissue")
                self.surf_tissue = widgets.Select(
                    choices=self.embryo.all_tissues, value=self.embryo.all_tissues[0]
                )
                select_surf_label = widgets.Container(
                    widgets=[surf_label, self.surf_tissue],
                )
                surf_run = widgets.FunctionGui(
                    show_surf, 
                    call_button="Compute and show surface"
                )
                surf_container = widgets.Container(
                    widgets=[
                        select_surf_label,
                        surf_run,
                    ],
                    layout="vertical",
                )
            else:
                surf_container = widgets.Container()
                logging.warning(
                    "pyvista is not installed. No surfaces can be generated.\n"
                    "Try pip install pyvista or conda install pyvista to install it."
                )
            return surf_container
        
        surf_tab = QTabWidget()
        surf_tab.setObjectName("Surface")
        surf_tab.addTab(select_surf().native, "Select Surface")
        return surf_tab

    def annotate_tab(self):
        def annotate():
            points = self.viewer.layers.selection.active
            selected_id = list(points.selected_data)
            selected_points = points.data[selected_id]
        
            adata = self.embryo.adata.copy()
            selected_points = np.array(selected_points)
            mask = np.isin(adata.obsm[self.embryo.coordinate_3d_key], selected_points).all(axis=1)

            if column_name.value not in adata.obs.columns:
                adata.obs[column_name.value] = adata.obs[self.embryo.tissue_name].copy()
                
            if not adata.obs[column_name.value].dtype.name == 'category':
                adata.obs[column_name.value] = adata.obs[column_name.value].astype('str')
                adata.obs[column_name.value] = adata.obs[column_name.value].astype('category')

            cat = adata.obs[column_name.value].cat.categories
            if cluster_anno.value not in cat:
                new_cat = sorted(list(cat) + [cluster_anno.value])
                adata.obs[column_name.value] = adata.obs[column_name.value].cat.set_categories(new_cat)
            adata.obs.loc[mask, column_name.value] = cluster_anno.value

            self.embryo.adata_anno = adata
            print(adata.obs[column_name.value].value_counts())

        def save_annotations():
            path = save_path.value
            self.embryo.adata_anno.obs[column_name.value] = self.embryo.adata_anno.obs[column_name.value].cat.remove_unused_categories()
            self.embryo.adata_anno.write_h5ad(path)
            print(f"adata saved to {path}")

        path = os.getcwd()
        run_annotation = widgets.FunctionGui(
            annotate, call_button="Annotation to selected points"
        )
        run_save = widgets.FunctionGui(
            save_annotations, call_button="Save Annotations"
        )
        cluster_anno = widgets.LineEdit(value='cluster 1',label="Cluster Name")
        column_name = widgets.LineEdit(value='new column 1', label="Column Name")
        save_path = widgets.LineEdit(value=os.path.join(path, 'napari.h5ad'), label="Save Path")
        annotation_container = widgets.Container(
            widgets=[
                cluster_anno,
                column_name,
                run_annotation,
                save_path,
                run_save
            ],
        )
        annotate_tab = QTabWidget()
        annotate_tab.setObjectName("Annotate")
        annotate_tab.addTab(annotation_container.native, "Annotate")
        return annotate_tab

    def one_gene_tab(self):
        viewer = self.viewer
        adata = self.embryo.adata
        def apply_cmap():
            """
            Apply a color map to cells
            """
            points = viewer.layers.selection.active
            if (
                    points is None
                    or points.as_layer_data_tuple()[-1] != "points"
                    or len(points.properties) == 0
            ):
                error_points_selection(show=True)
                return
            if points.face_color_mode.lower() != "colormap":
                points.face_color_mode = "colormap"
            if not self.cmap_check.value:
                points.face_colormap = self.cmap.value
                points.mplcmap = None
            else:
                init_value = self.grey.value
                cmap_mpl = {
                    "red": [[0.0, init_value, init_value], [1.0, 0.0, 0.0]],
                    "blue": [[0.0, init_value, init_value], [1.0, 0.0, 0.0]],
                    "green": [[0.0, init_value, init_value], [1.0, 0.0, 0.0]],
                }
                cmap_mpl[self.manual_color.value.lower()] = [
                    [0.0, init_value, init_value],
                    [1.0, 1.0, 1.0],
                ]
                if self.manual_color.value == "Red":
                    color = 0
                elif self.manual_color.value == "Green":
                    color = 1
                else:
                    color = 2
                cmap_val = [
                    [init_value, init_value, init_value, 1],
                    [0, 0, 0, 1],
                ]
                cmap_val[1][color] = 1
                cmap = Colormap(cmap_val)
                mplcmap = colors.LinearSegmentedColormap("Manual cmap", cmap_mpl)
                points.mplcmap = mplcmap
                points.face_colormap = cmap
            points.refresh()

        def adj_int():
            """
            Adjust the intensity for gene expression colouring
            """
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return
            min = self.adj_int_low.value
            max = self.adj_int_high.value
            if max < min:
                max, min = min, max
            min_exp,max_exp = self.min_exp, self.max_exp
            min_actrual = (min * (max_exp - min_exp)) + min_exp
            max_actrual = (max * (max_exp - min_exp)) + min_exp
            points.face_contrast_limits = (min_actrual, max_actrual)
            points.refresh()

        def threshold():
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return
            min_v = min(self.threshold_low.value, self.threshold_high.value)
            max_v = max(self.threshold_low.value, self.threshold_high.value)
            gene = self.gene.value
            gene_exp = safe_toarray(adata[:, gene].X)[:,0]
            min_exp, max_exp = gene_exp.min(), gene_exp.max()
            gene_exp_norm = (gene_exp - min_exp) / (max_exp - min_exp)
            gene_exp_norm = np.clip(gene_exp_norm, 0.0, 1.0)
            mask = (gene_exp_norm >= min_v) & (gene_exp_norm <= max_v)
            shown_ori = self.mask_filter
            mask_final = np.logical_and(shown_ori, mask)
            points.shown = mask_final
            points.refresh()
            self.threshold_output.value = f"Showing {mask_final.sum()} cells out of {len(mask_final)}"

        def show_gene():
            """
            Colour cells according to their gene expression
            """
            points = viewer.layers.selection.active
            gene = self.gene.value
            gene_exp = safe_toarray(adata[:, gene].X)[:,0]
            gene_exp = np.nan_to_num(gene_exp, nan=0.0, posinf=np.max(gene_exp), neginf=0.0)
            min_exp, max_exp = gene_exp.min(), gene_exp.max()
            gene_exp_norm = (gene_exp - min_exp) / (max_exp - min_exp)
            gene_exp_norm = np.clip(gene_exp_norm, 0.0, 1.0)
            features = {}
            features[f'gene_exp_{gene}'] = gene_exp
            if hasattr(self, 'moransI'):
                features[f'morans_I_{gene}'] = self.moransI[gene]
            colors = ALL_COLORMAPS[self.cmap.value]
            points.face_color = colors.map(gene_exp_norm)
            points.features = features
            points.refresh()
            self.min_exp = min_exp
            self.max_exp = max_exp

        def show_similar_genes_exp():
            """
            Show the expression of the selected similar gene.
            """
            points = viewer.layers.selection.active
            selected_gene = self.select_gene.value
            gene_exp = safe_toarray(adata[:, selected_gene].X)[:,0]
            gene_exp = np.nan_to_num(gene_exp, nan=0.0, posinf=np.max(gene_exp), neginf=0.0)
            min_exp, max_exp = gene_exp.min(), gene_exp.max()
            gene_exp_norm = (gene_exp - min_exp) / (max_exp - min_exp)
            gene_exp_norm = np.clip(gene_exp_norm, 0.0, 1.0)
            features = {}
            features[f'gene_exp_{selected_gene}'] = gene_exp
            colors = ALL_COLORMAPS[self.cmap.value]
            points.face_color = colors.map(gene_exp_norm)
            points.features = features
            points.refresh()

        def show_similar_genes():
            all_gene_exp = safe_toarray(adata.X).T
            gene_exp = safe_toarray(adata[:, self.gene.value].X)[:,0]
            similarity_list = cosine_similarity(all_gene_exp, gene_exp.reshape(1, -1)).flatten()
            similarity_dict = {
                adata.var_names[i]: similarity_list[i]
                for i in range(len(adata.var_names))
            }
            sorted_genes = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)
            self.similar_genes = [gene for gene, _ in sorted_genes if gene != self.gene.value][:10]
            self.select_gene.choices = self.similar_genes
        
        def container():
            """
            Create a container for the one gene tab.
            """
            self.gene = widgets.LineEdit(
                value=self.selected_adata.var_names[0],
                label="Gene",
            )
            self.threshold_low = widgets.FloatSpinBox(
                value=0.0, min=0.0, max=1.0, step=0.01,label="Low value"
            )
            self.threshold_high = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1.0, step=0.01, label="High value"
            )
            self.threshold_output = widgets.Label(value="")
            threshold_run = widgets.FunctionGui(
                threshold, call_button="Apply Threshold"
            )
            threshold_container = widgets.Container(
                widgets=[
                    self.threshold_low,
                    self.threshold_high,
                    threshold_run,
                    self.threshold_output,
                ],
                layout="vertical",
            )
            self.cmap = widgets.ComboBox(choices=ALL_COLORMAPS.keys())
            self.cmap.changed.connect(apply_cmap)
            text_manual = widgets.Label(value="Manual:")
            self.cmap_check = widgets.CheckBox(value=False)
            grey_text = widgets.Label(value="Start Grey:")
            self.grey = widgets.FloatSpinBox(value=0.2, min=0, max=1, step=0.01)
            color_text = widgets.Label(value="Main color")
            self.manual_color = widgets.ComboBox(choices=["Red", "Green", "Blue"])
            cmap_check = widgets.Container(
                widgets=[text_manual, self.cmap_check, grey_text, self.grey],
                layout="horizontal",
                labels=False,
            )
            manual_color = widgets.Container(
                widgets=[color_text, self.manual_color],
                layout="horizontal",
                labels=False,
            )
            cmap_man_run = widgets.FunctionGui(
                apply_cmap, call_button="Apply color map"
            )
            cmap_container = widgets.Container(
                widgets=[self.cmap, cmap_check, manual_color, cmap_man_run],
                labels=False,
            )
            self.adj_int_low = widgets.FloatSlider(min=0, max=1, value=0,label="Low Intensity")
            self.adj_int_high = widgets.FloatSlider(min=0, max=1, value=1,label="High Intensity")
            adj_int_run = widgets.FunctionGui(
                adj_int, call_button="Adjust contrast"
            )
            adj_label = widgets.Label(value="run color map first\nonly turn min bigger and max smaller")
            adj_int_container = widgets.Container(
                widgets=[self.adj_int_low, self.adj_int_high, adj_int_run, adj_label],
                labels=False,
            )

            little_tab = QTabWidget()
            little_tab.addTab(threshold_container.native, "Threshold")
            little_tab.addTab(cmap_container.native, "Colormap")
            little_tab.addTab(adj_int_container.native, "Adjust Contrast")
            little_tab.native = little_tab
            little_tab.name = ''

            run_show_flatten = widgets.FunctionGui(
                self.show_flatten,
                call_button="Show in Flatten",
                layout="vertical",
            )
            run_show_gene = widgets.FunctionGui(
                show_gene,
                call_button="Show Gene",
                layout="vertical",
            )
            run_show_similar_genes = widgets.FunctionGui(
                show_similar_genes,
                call_button="Show Similar Genes",
                layout="vertical",
            )
            if hasattr(self, 'similar_genes'):
                similar_genes = self.similar_genes
            else:
                similar_genes = [self.gene.value]
            self.select_gene = widgets.Select(
                choices=similar_genes,
                value=similar_genes[0],
                label="Select Similar Gene",
                )
            run_show_similar_genes_exp = widgets.FunctionGui(
                show_similar_genes_exp,
                call_button="Show Similar Gene Exp",
                layout="vertical",
            )
            container = widgets.Container(
                widgets=[
                    self.gene,
                    little_tab,
                    run_show_gene,
                    run_show_flatten,
                    run_show_similar_genes,
                    self.select_gene,
                    run_show_similar_genes_exp,
                    ],
                layout="vertical",
                labels=False,
            )
            return container
        
        one_gene_tab = QTabWidget()
        one_gene_tab.addTab(container().native,'Select Gene')

        return one_gene_tab
    
    def two_genes_tab(self):
        viewer = self.viewer
        adata = self.embryo.adata
        def show_two_genes():
            """
            Colour cells according to their gene expression
            """
            points = viewer.layers.selection.active
            gene_1 = self.gene_1.value
            gene_2 = self.gene_2.value
            gene_exp_1 = safe_toarray(adata[:, gene_1].X)[:,0]
            gene_exp_2 = safe_toarray(adata[:, gene_2].X)[:,0]
            min_exp_1, max_exp_1 = gene_exp_1.min(), gene_exp_1.max()
            min_exp_2, max_exp_2 = gene_exp_2.min(), gene_exp_2.max()
            with np.errstate(divide='ignore', invalid='ignore'):
                gene_exp_norm_1 = np.clip((gene_exp_1 - min_exp_1) / (max_exp_1 - min_exp_1), 0, 1)
                gene_exp_norm_2 = np.clip((gene_exp_2 - min_exp_2) / (max_exp_2 - min_exp_2), 0, 1)
            colors = np.zeros((len(gene_exp_norm_1), 3))
            colors[:, 0] = gene_exp_norm_1
            colors[:, 2] = gene_exp_norm_2
            features = {}
            features[f'gene_exp_{gene_1}'] = gene_exp_1
            features[f'gene_exp_{gene_2}'] = gene_exp_2
            if hasattr(self, 'moransI'):
                features[f'morans_I_{gene_1}'] = self.moransI[gene_1]
                features[f'morans_I_{gene_2}'] = self.moransI[gene_2]
            points.face_color = colors
            points.features = features
            points.refresh()
            self.color_2g = colors

        def threshold_2gene():
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return
            gene_1 = self.gene_1.value
            gene_2 = self.gene_2.value
            gene_exp_1 = safe_toarray(adata[:, gene_1].X)[:,0]
            gene_exp_2 = safe_toarray(adata[:, gene_2].X)[:,0]
            min_exp_1, max_exp_1 = gene_exp_1.min(), gene_exp_1.max()
            min_exp_2, max_exp_2 = gene_exp_2.min(), gene_exp_2.max()
            with np.errstate(divide='ignore', invalid='ignore'):
                gene_exp_norm_1 = np.clip((gene_exp_1 - min_exp_1) / (max_exp_1 - min_exp_1), 0, 1)
                gene_exp_norm_2 = np.clip((gene_exp_2 - min_exp_2) / (max_exp_2 - min_exp_2), 0, 1)
            min_v_1 = self.threhold_1_min.value
            max_v_1 = self.threhold_1_max.value
            min_v_2 = self.threhold_2_min.value
            max_v_2 = self.threhold_2_max.value
            if max_v_1 < min_v_1:
                max_v_1, min_v_1 = min_v_1, max_v_1
            mask = (gene_exp_norm_1 >= min_v_1) & (gene_exp_norm_1 <= max_v_1) & \
                   (gene_exp_norm_2 >= min_v_2) & (gene_exp_norm_2 <= max_v_2)
            shown_ori = self.mask_filter
            mask_final = np.logical_and(shown_ori, mask)
            points.shown = mask_final
            self.threshold_output_2g.value = f"Showing {mask_final.sum()} cells out of {len(mask_final)}"
            points.refresh()
            
        def adj_int():
            """
            Adjust the intensity for gene expression colouring
            """
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return  
            colors = self.color_2g.copy()
            low_int = self.adj_int_low_2g.value
            high_int = self.adj_int_high_2g.value
            r = colors[:, 0]
            g = colors[:, 1]
            b = colors[:, 2]
            I = 0.299 * r + 0.587 * g + 0.114 * b
            I = np.clip(I, 0, 1)
            low_mask = I < low_int
            high_mask = I > high_int
            mid_mask = (~low_mask) & (~high_mask)
            colors[low_mask] = [0, 0, 0]
            if colors.shape[1] == 4:
                colors[low_mask, 3] = 1
            colors[high_mask] = [1, 0, 1]
            if colors.shape[1] == 4:
                colors[high_mask, 3] = 1
            scale =(high_int - low_int)
            r_mid = (r[mid_mask] - low_int) / scale
            g_mid = (g[mid_mask] - low_int) / scale
            b_mid = (b[mid_mask] - low_int) / scale
            colors[mid_mask, 0] = np.clip(r_mid, 0, 1)
            colors[mid_mask, 1] = np.clip(g_mid, 0, 1)
            colors[mid_mask, 2] = np.clip(b_mid, 0, 1)
            points.face_color = colors
            points.refresh()

        def container():
            """
            Create a container for the two genes tab.
            """
            adata = self.selected_adata
            self.gene_1 = widgets.LineEdit(
                value=adata.var_names[0],
                label="Gene 1",
            )
            self.threhold_1_min = widgets.FloatSpinBox(
                value=0.0, min=0.0, max=1,
                step=0.01, label="Threshold 1 min"
            )
            self.threhold_1_max = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1,
                step=0.01, label="Threshold 2 max"
            )
            self.gene_2 = widgets.LineEdit(
                value=adata.var_names[1],
                label="Gene 2",
            )
            self.threhold_2_min = widgets.FloatSpinBox(
                value=0, min=0.0, max=1,
                step=0.01, label="Threshold 2 min"
            )
            self.threhold_2_max = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1,
                step=0.01, label="Threshold 2 max"
            )
            self.threshold_output_2g = widgets.Label(value="")
            note_adj_int_2g = widgets.Label(
                value="I = 0.299 * R + 0.587 * G + 0.114 * B"
            )
            self.adj_int_low_2g = widgets.FloatSlider(
                min=0, max=1, value=0, label="Low Intensity"
            )
            self.adj_int_high_2g = widgets.FloatSlider(
                min=0, max=1, value=1, label="High Intensity"
            )
            run_adj_int_2g = widgets.FunctionGui(
                adj_int, call_button="Adjust Contrast"
            )
            run_show_two_genes = widgets.FunctionGui(
                show_two_genes,
                call_button="Show Two Genes",
                layout="vertical",
            )
            run_threshold_2gene = widgets.FunctionGui(
                threshold_2gene,
                call_button="Apply Threshold",
            )
            run_show_flatten = widgets.FunctionGui(
                self.show_flatten,
                call_button="Show in Flatten",
            )
            container = widgets.Container(
                widgets=[
                    self.gene_1,
                    self.threhold_1_min,
                    self.threhold_1_max,
                    self.gene_2,
                    self.threhold_2_min,
                    self.threhold_2_max,
                    self.threshold_output_2g,
                    run_show_two_genes,
                    note_adj_int_2g,
                    self.adj_int_low_2g,
                    self.adj_int_high_2g,
                    run_adj_int_2g,
                    run_threshold_2gene,
                    run_show_flatten,
                ],
                layout="vertical",
            )
            return container
        
        two_genes_tab = QTabWidget()
        two_genes_tab.addTab(container().native, 'Select Two Genes')
        return two_genes_tab
    
    def three_genes_tab(self):
        viewer = self.viewer
        adata = self.embryo.adata
        def show_three_genes():
            """
            Colour cells according to their gene expression
            """
            points = viewer.layers.selection.active
            gene_1 = self.gene_3.value
            gene_2 = self.gene_4.value
            gene_3 = self.gene_5.value
            gene_exp_1 = safe_toarray(adata[:, gene_1].X)[:,0]
            gene_exp_2 = safe_toarray(adata[:, gene_2].X)[:,0]
            gene_exp_3 = safe_toarray(adata[:, gene_3].X)[:,0]
            min_exp_1, max_exp_1 = gene_exp_1.min(), gene_exp_1.max()
            min_exp_2, max_exp_2 = gene_exp_2.min(), gene_exp_2.max()
            min_exp_3, max_exp_3 = gene_exp_3.min(), gene_exp_3.max()
            with np.errstate(divide='ignore', invalid='ignore'):
                gene_exp_norm_1 = np.clip((gene_exp_1 - min_exp_1) / (max_exp_1 - min_exp_1), 0, 1)
                gene_exp_norm_2 = np.clip((gene_exp_2 - min_exp_2) / (max_exp_2 - min_exp_2), 0, 1)
                gene_exp_norm_3 = np.clip((gene_exp_3 - min_exp_3) / (max_exp_3 - min_exp_3), 0, 1)
            colors = np.zeros((len(gene_exp_norm_1), 3))
            colors[:, 0] = gene_exp_norm_1
            colors[:, 1] = gene_exp_norm_2
            colors[:, 2] = gene_exp_norm_3
            features = {}
            features[f'gene_exp_{gene_1}'] = gene_exp_1
            features[f'gene_exp_{gene_2}'] = gene_exp_2
            features[f'gene_exp_{gene_3}'] = gene_exp_3
            if hasattr(self, 'moransI'):
                features[f'morans_I_{gene_1}'] = self.moransI[gene_1]
                features[f'morans_I_{gene_2}'] = self.moransI[gene_2]
                features[f'morans_I_{gene_3}'] = self.moransI[gene_3]
            points.face_color = colors
            points.features = features
            points.refresh()
            self.color_3g = colors

        def threshold_3gene():
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return
            gene_1 = self.gene_3.value
            gene_2 = self.gene_4.value
            gene_3 = self.gene_5.value
            gene_exp_1 = safe_toarray(adata[:, gene_1].X)[:,0]
            gene_exp_2 = safe_toarray(adata[:, gene_2].X)[:,0]
            gene_exp_3 = safe_toarray(adata[:, gene_3].X)[:,0]
            min_exp_1, max_exp_1 = gene_exp_1.min(), gene_exp_1.max()
            min_exp_2, max_exp_2 = gene_exp_2.min(), gene_exp_2.max()
            min_exp_3, max_exp_3 = gene_exp_3.min(), gene_exp_3.max()
            with np.errstate(divide='ignore', invalid='ignore'):
                gene_exp_norm_1 = np.clip((gene_exp_1 - min_exp_1) / (max_exp_1 - min_exp_1), 0, 1)
                gene_exp_norm_2 = np.clip((gene_exp_2 - min_exp_2) / (max_exp_2 - min_exp_2), 0, 1)
                gene_exp_norm_3 = np.clip((gene_exp_3 - min_exp_3) / (max_exp_3 - min_exp_3), 0, 1)
            min_v_1 = self.threshold_3_min.value
            max_v_1 = self.threshold_3_max.value
            min_v_2 = self.threshold_4_min.value
            max_v_2 = self.threshold_4_max.value
            min_v_3 = self.threshold_5_min.value
            max_v_3 = self.threshold_5_max.value
            if max_v_1 < min_v_1:
                max_v_1, min_v_1 = min_v_1, max_v_1
            if max_v_2 < min_v_2:
                max_v_2, min_v_2 = min_v_2, max_v_2
            if max_v_3 < min_v_3:
                max_v_3, min_v_3 = min_v_3, max_v_3
            mask = (gene_exp_norm_1 >= min_v_1) & (gene_exp_norm_1 <= max_v_1) & \
                   (gene_exp_norm_2 >= min_v_2) & (gene_exp_norm_2 <= max_v_2) & \
                   (gene_exp_norm_3 >= min_v_3) & (gene_exp_norm_3 <= max_v_3)
            shown_ori = self.mask_filter
            mask_final = np.logical_and(shown_ori, mask)
            points.shown = mask_final
            self.threshold_output_3g.value = f"Showing {mask_final.sum()} cells out of {len(mask_final)}"
            points.refresh()

        def adj_int():
            """
            Adjust the intensity for gene expression colouring
            """
            points = viewer.layers.selection.active
            if points is None or points.as_layer_data_tuple()[-1] != "points":
                error_points_selection(show=True)
                return  
            colors = self.color_3g.copy()
            low_int = self.adj_int_low_3g.value
            high_int = self.adj_int_high_3g.value
            r = colors[:, 0]
            g = colors[:, 1]
            b = colors[:, 2]
            I = 0.299 * r + 0.587 * g + 0.114 * b
            I = np.clip(I, 0, 1)
            low_mask = I < low_int
            high_mask = I > high_int
            mid_mask = (~low_mask) & (~high_mask)
            r_max = np.max(r)
            g_max = np.max(g)
            b_max = np.max(b)
            colors[low_mask] = [0, 0, 0]
            if colors.shape[1] == 4:
                colors[low_mask, 3] = 1
            colors[high_mask] = [r_max, g_max, b_max]
            if colors.shape[1] == 4:
                colors[high_mask, 3] = 1
            scale =(high_int - low_int)
            r_mid = (r[mid_mask] - low_int) / scale
            g_mid = (g[mid_mask] - low_int) / scale
            b_mid = (b[mid_mask] - low_int) / scale
            colors[mid_mask, 0] = np.clip(r_mid, 0, 1)
            colors[mid_mask, 1] = np.clip(g_mid, 0, 1)
            colors[mid_mask, 2] = np.clip(b_mid, 0, 1)
            points.face_color = colors
            points.refresh()

        def container():
            """
            Create a container for the three genes tab.
            """
            self.gene_3 = widgets.LineEdit(
                value=adata.var_names[0],
                label="Gene 1",
            )
            self.threshold_3_min = widgets.FloatSpinBox(
                value=0.0, min=0.0, max=1,
                step=0.01, label="Threshold 1 min"
            )
            self.threshold_3_max = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1,
                step=0.01, label="Threshold 1 max"
            )
            self.gene_4 = widgets.LineEdit(
                value=adata.var_names[1],
                label="Gene 2",
            )
            self.threshold_4_min = widgets.FloatSpinBox(
                value=0, min=0.0, max=1,
                step=0.01, label="Threshold 2 min"
            )
            self.threshold_4_max = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1,
                step=0.01, label="Threshold 2 max"
            )
            self.gene_5 = widgets.LineEdit(
                value=adata.var_names[2],
                label="Gene 3",
            )
            self.threshold_5_min = widgets.FloatSpinBox(
                value=0, min=0.0, max=1,
                step=0.01, label="Threshold 3 min"
            )
            self.threshold_5_max = widgets.FloatSpinBox(
                value=1.0, min=0.0, max=1,
                step=0.01, label="Threshold 3 max"
            )
            self.threshold_output_3g = widgets.Label(value="")
            self.adj_int_low_3g = widgets.FloatSlider(
                min=0, max=1, value=0, label="Low Intensity"
            )
            self.adj_int_high_3g = widgets.FloatSlider(
                min=0, max=1, value=1, label="High Intensity"
            )
            run_adj_int_3g = widgets.FunctionGui(
                adj_int, call_button="Adjust Contrast"
            )
            run_show_three_genes = widgets.FunctionGui(
                show_three_genes,
                call_button="Show Three Genes",
                layout="vertical",
            )
            run_threshold_3gene = widgets.FunctionGui(
                threshold_3gene,
                call_button="Apply Threshold",
            )
            run_show_flatten = widgets.FunctionGui(
                self.show_flatten,
                call_button="Show Flatten",
            )
            container = widgets.Container(
                widgets=[
                    self.gene_3,
                    self.threshold_3_min,
                    self.threshold_3_max,
                    self.gene_4,
                    self.threshold_4_min,
                    self.threshold_4_max,
                    self.gene_5,
                    self.threshold_5_min,
                    self.threshold_5_max,
                    self.threshold_output_3g,
                    run_show_three_genes,
                    self.adj_int_low_3g,
                    self.adj_int_high_3g,
                    run_adj_int_3g,
                    run_threshold_3gene,
                    run_show_flatten,
                ],
                layout="vertical",
            )
            return container
        
        three_genes_tab = QTabWidget()
        three_genes_tab.addTab(container().native, 'Select Three Genes')
        return three_genes_tab
    
    def umap_tab(self):
        """
        Function that builds the qt container for the umap
        """
        gene_label = widgets.Label(value="Choose gene")
        gene = widgets.LineEdit(value=self.select_gene.value)

        tissues_label = widgets.Label(value="Display tissues umap")
        tissues = widgets.CheckBox(value=False)

        variable_genes_label = widgets.Label(value="Take only variable genes")
        variable_genes = widgets.CheckBox(value=True)

        stats_label = widgets.Label(value="Statistic for\nchoosing distributions")
        stats = widgets.RadioButtons(
            choices=["Standard Deviation", "Mean", "Median"],
            value="Standard Deviation",
        )
        self.umap_selec = UmapSelection(
            self.viewer,
            self.embryo,
            gene,
            tissues,
            stats,
            variable_genes,
            self.tissue_color_map,
        )
        umap_run = widgets.FunctionGui(
            self.umap_selec.run, call_button="Show gene on Umap", name=""
        )

        gene_container = widgets.Container(
            widgets=[gene_label, gene], labels=False, layout="horizontal"
        )
        variable_genes_container = widgets.Container(
            widgets=[variable_genes_label, variable_genes],
            labels=False,
            layout="horizontal",
        )
        tissues_container = widgets.Container(
            widgets=[tissues_label, tissues], labels=False, layout="horizontal"
        )
        stats_container = widgets.Container(
            widgets=[stats_label, stats], labels=False, layout="horizontal"
        )
        umap_container = widgets.Container(
            widgets=[
                gene_container,
                tissues_container,
                variable_genes_container,
                stats_container,
                umap_run,
            ],
            labels=False,
        )
        umap_tab = QTabWidget()
        umap_tab.addTab(umap_container.native, "Umap")
        return umap_tab
    
    def Moran_tab(self):
        """
        Function that builds the qt container for the Moran's I
        """
        viewer = self.viewer
        def compute_moran():
            adata = self.selected_adata
            geneslist1, num1 = sc.pp.filter_genes(self.selected_adata, min_counts=self.min_counts.value,inplace=False)
            geneslist2, num2 = sc.pp.filter_genes(self.selected_adata, min_cells=self.min_cells.value*self.embryo.adata.obs.shape[0], inplace=False)
            geneslist3, num3 = sc.pp.filter_genes(self.selected_adata, max_cells=self.max_cells.value*self.embryo.adata.obs.shape[0], inplace=False)
            geneslist = [a and b and c for a, b, c in zip(geneslist1, geneslist2, geneslist3)]
            adata = self.selected_adata[:, geneslist]
            self.threshold_output_moran.value = f"computer Moran's I for {len(adata)} cells"
            sq.gr.spatial_neighbors(adata, spatial_key=self.embryo.coordinate_3d_key,key_added='spatial')
            Moranres = sq.gr.spatial_autocorr(adata, mode="moran", copy = True)
            self.moransI = Moranres["I"]
            moran_idx = Moranres["I"][:10000].index.tolist()
            moran_values = Moranres["I"][:10000].values.tolist()
            gene_exp = safe_toarray(adata[:, moran_idx].X)
            gene_count_cell = np.count_nonzero(gene_exp,axis=0)
            choice = [f"{gene} ({value:.6f})[n_cells:{cell}]" for gene, value,cell in zip(moran_idx, moran_values,gene_count_cell)]
            self.moran_gene.choices = choice
        
        def plot_moran():
            if self.moran_gene.value == 'compute Moran\'s I first' or len(self.moran_gene.value) == 0:
                return
            else:
                points = viewer.layers.selection.active
                if isinstance (self.moran_gene.value, str):
                    gene = self.moran_gene.value.split(' (')[0]
                else:
                    gene = self.moran_gene.value[0].split(' (')[0]
                gene_exp = safe_toarray(self.embryo.adata[:, gene].X)[:,0]
                min_exp, max_exp = gene_exp.min(), gene_exp.max()
                gene_exp_norm = (gene_exp - min_exp) / (max_exp - min_exp)
                features = {}
                features[f'gene_exp_{gene}'] = gene_exp
                colors = ALL_COLORMAPS[self.cmap.value]
                points.face_color = colors.map(gene_exp_norm)
                points.features = features
                points.refresh()

        def show_moran():
            self.min_counts = widgets.FloatSpinBox(
                value=0.0, min=0.0, max=100.0, step=0.01,
                label="Minimum count for per gene"
            )
            self.min_cells = widgets.FloatSpinBox(
                value=0, min=0, max=1, step=0.01,
                label="Floor precentage of n_cells"
            )
            self.max_cells = widgets.FloatSpinBox(
                value=1, min=0, max=1, step=0.01,
                label="Ceiling precentage of n_cells"
            )
            self.threshold_output_moran = widgets.Label(value="")
            run_moran = widgets.FunctionGui(
                compute_moran,
                call_button="Show Moran's I",
                layout="vertical",
            )
            self.moran_gene = widgets.Select(
                choices=['compute Moran\'s I first'],
                value='compute Moran\'s I first',
                label="Select a gene\nto see exp",
                allow_multiple=False,
            )
            self.moran_gene.changed.connect(plot_moran)
            moran_container = widgets.Container(
                widgets=[
                    self.min_counts,
                    self.min_cells,
                    self.max_cells,
                    self.threshold_output_moran,
                    run_moran,
                    self.moran_gene,
                ],
                layout="vertical",
            )
            return moran_container

        moran_tab = QTabWidget()
        moran_tab.addTab(show_moran().native, "Moran's I")

        return moran_tab
    
    def diff_exp_tab(self):
        """
        Function that builds the qt container for the differential expression
        """
        viewer = self.viewer
        def compute_diff_exp():
            adata = self.selected_adata
            diff_tissue = self.diff_tissue.value
            if diff_tissue[0] in adata.obs[self.embryo.tissue_name].unique():
                diff_adata = adata[adata.obs[self.embryo.tissue_name] == diff_tissue[0]]
            else:
                logging.warning(f"Tissue {diff_tissue} not found in adata.obs[{self.embryo.tissue_name}].")
                return
            diff_gene_avg = safe_toarray(diff_adata.X).mean(axis=0)
            all_gene_avg = safe_toarray(adata.X).mean(axis=0)
            epsilon = 0.0001
            SES = np.log2((diff_gene_avg + epsilon) / (all_gene_avg + epsilon))
            SES_dict = {
                adata.var_names[i]: SES[i]
                for i in range(len(adata.var_names))
            }
            sorted_genes = sorted(SES_dict.items(), key=lambda x: x[1], reverse=True)
            diff_25_idx = [gene for gene, _ in sorted_genes[:25]]
            diff_25_values = [SES_dict[gene] for gene in diff_25_idx]
            gene_count_cell = np.count_nonzero(safe_toarray(adata[:, diff_25_idx].X), axis=0)
            self.diff_exp_gene.choices = [f"{gene} ({value:.6f})[n_cells:{cell}]" for gene, value,cell in zip(diff_25_idx, diff_25_values,gene_count_cell)]
        def plot_diff_exp():
            points = viewer.layers.selection.active
            if isinstance(self.diff_exp_gene.value, list) and len(self.diff_exp_gene.value) > 0:
                gene_str = self.diff_exp_gene.value[0]
            else:
                gene_str = self.diff_exp_gene.value
            gene = gene_str.split(' (')[0]
            gene_exp = safe_toarray(self.embryo.adata[:, gene].X)[:,0]
            min_exp, max_exp = gene_exp.min(), gene_exp.max()
            gene_exp_norm = (gene_exp - min_exp) / (max_exp - min_exp)
            features = {}
            features[f'gene_exp_{gene}'] = gene_exp
            colors = ALL_COLORMAPS[self.cmap.value]
            points.face_color = colors.map(gene_exp_norm)
            points.features = features
            points.refresh()
        
        def show_diff_exp():
            self.diff_tissue = widgets.Select(
                choices=self.embryo.all_tissues,
                value=self.embryo.all_tissues[0],
                label="Select tissue for\ndifferential expression",
                allow_multiple=False,
            )
            run_diff_exp = widgets.FunctionGui(
                compute_diff_exp,
                call_button="Show top 25 Differential Expression",
                layout="vertical",
            )
            self.diff_exp_gene = widgets.Select(
                choices=[''],
                value='',
                label="Select a gene\nto see exp",
            )
            run_show_diff_exp = widgets.FunctionGui(
                plot_diff_exp,
                call_button="Show chosed top 25 gene exp",
                layout="vertical",
            )
            diff_exp_container = widgets.Container(
                widgets=[
                    self.diff_tissue,
                    run_diff_exp,
                    self.diff_exp_gene,
                    run_show_diff_exp,
                ],
                layout="vertical",
            )
            return diff_exp_container

        diff_exp_tab = QTabWidget()
        diff_exp_tab.addTab(show_diff_exp().native, "Diff Exp")

        return diff_exp_tab
    def create_widget(self):
        '''
        Create UI
        '''
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        main_tab = QTabWidget()

        tab_1 = QTabWidget()
        tab_1.addTab(self.legend_tab(), "Legend")
        tab_1.addTab(self.tissue_tab(), "Tissue")
        tab_1.addTab(self.slice_tab(), "Slice")
        tab_1.addTab(self.germ_layer_tab(), "Germ Layer")
        tab_1.addTab(self.selectXY_tab(), "Select XYZ")
        tab_1.addTab(self.surface_tab(), "Surface")
        tab_1.addTab(self.annotate_tab(), "Annotate")
        main_tab.addTab(tab_1, "Visualization")

        tab_2 = QTabWidget()
        tab_2.addTab(self.one_gene_tab(), "1 Gene")
        tab_2.addTab(self.two_genes_tab(), "2 Genes")
        tab_2.addTab(self.three_genes_tab(), "3 Genes")
        # tab_2.addTab(self.umap_tab(), "UMAP")
        tab_2.addTab(self.Moran_tab(), "Moran's I")
        tab_2.addTab(self.diff_exp_tab(), "Diff Exp")
        main_tab.addTab(tab_2, "Analysis")

        # tab_3 = QTabWidget()
        # main_tab.addTab(tab_3, "Scanpy plots")

        layout.addWidget(main_tab)
        self.viewer.window.add_dock_widget(
            container, name="Embryo Display", area="right"
        )

    def display(self):
        """
        Display the Embryo data in the napari viewer.
        """
        adata = self.embryo.adata
        tissue_types = adata.obs[self.embryo.tissue_name].astype(str).values
        self.viewer.dims.ndisplay = 3
        position = adata.obsm[self.embryo.coordinate_3d_key]
        self.viewer.add_points(
            position,
            size=10,
            face_color=[self.tissue_color_map[t] for t in tissue_types],
            features=adata.obs,
        )

    def __init__(self, viewer, embryo):
        """
        Initialize the DisplayEmbryo object with the given parameters.

        Args:
            embryo (Embryo): An instance of the Embryo class.
            viewer (napari.Viewer): The napari viewer instance.
        """
        self.embryo = embryo
        self.viewer = viewer
        if self.embryo.adata.obsm[self.embryo.coordinate_3d_key].shape[1] != 3 and 'z' in self.embryo.adata.obs.columns:
            self.embryo.adata.obsm[self.embryo.coordinate_3d_key] = np.column_stack(
                [
                    self.embryo.adata.obsm[self.embryo.coordinate_3d_key][:, 0],
                    self.embryo.adata.obsm[self.embryo.coordinate_3d_key][:, 1],
                    self.embryo.adata.obs['z'].values,
                ]
            )
        self.selected_adata = self.embryo.adata.copy()
        self.color_set()
        self.create_widget()
        self.display()
