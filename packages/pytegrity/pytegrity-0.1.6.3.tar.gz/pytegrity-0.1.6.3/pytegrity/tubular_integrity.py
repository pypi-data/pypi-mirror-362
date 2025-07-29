import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
import pandas as pd
import lasio as ls
import pyvista as pv
import numpy as np
import sklearn.cluster as cl



def plot_well_integrity(las_file_as_df: pd.DataFrame, fingers: list,
                        plotly_template="plotly_dark", height=1500, width=1000):
    """
    Generates a comprehensive interactive visualization of well integrity data
    using multiple Plotly subplots.

    Parameters
    ----------
    las_file_as_df : pd.DataFrame
        A dataframe representing the LAS file, containing logging data per depth.
        Must include a "GR" column (Gamma Ray) and finger log curves.
        
    fingers : list of str
        A list of column names (as strings) representing finger tool measurements.

    plotly_template : str, optional
        Plotly template to use for layout and color theme. Default is 'plotly_dark'.

    height : int, optional
        Height of the resulting figure in pixels. Default is 1500.

    width : int, optional
        Width of the resulting figure in pixels. Default is 1000.

    Returns
    -------
    fig : plotly.graph_objs._figure.Figure
        A Plotly figure containing:
        - GR log curve
        - Min, Max, Avg statistical curves for selected fingers
        - Overlaid finger logs as line traces (like seismic display)
        - 2D colored heatmap of finger values (depth vs. finger)

    Notes
    -----
    - Y-axis is reversed to reflect depth-based display.
    - Intended for well integrity diagnostics and quick multi-log inspection.
    - Supports thousands of data points with optimized rendering (Scattergl).
    """
    data = las_file_as_df
    fing = fingers

    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=("GR", "Statistics", "Fing/Pad", "2D Map"),
        horizontal_spacing=0.001,
        shared_yaxes=True
    )

    n_traces = len(fing)
    time = data.index
    trace_spacing = 1  # horizontal spacing between traces

    # Plot finger logs as shifted line traces (like seismic-style wiggles)
    finger_traces = []
    
    for i in range(n_traces):
        trace_data = data[fing[i]]
        x = trace_data + i * (trace_spacing * 0.2)
        
        finger_traces.append(go.Scattergl(
            x=x,
            y=list(range(len(data))),
            mode='lines',
            line=dict(color='blue', width=1),
            showlegend=False,
            name=fing[i]
        ))
    fig.add_traces(finger_traces,1,3)

    # Flip Y-axis globally
    # Prepare 2D matrix for heatmap
    trace_matrix = data[fing].to_numpy().T
    trace_matrix = trace_matrix.T

    map2d = px.imshow(
        trace_matrix,
        labels=dict(x="Readings", y="Depth", color="Amplitude"),
        aspect="auto",
        origin="upper",
        color_continuous_scale='Turbo'
    )

    # Plot statistical curves (Min, Max, Avg)
    min_curve = go.Line(x=data[fing].min(1), y=list(range(len(time))), name="Minimum", line_width=.51)
    max_curve = go.Line(x=data[fing].max(1), y=list(range(len(time))), name="Maximum", line_width=.51)
    avg_curve = go.Line(x=data[fing].mean(1), y=list(range(len(time))), name="Average", line_width=.51)
    gr = go.Line(x=data["GR"], y=list(range(len(time))), line_color="green", name="GR", line_width=.5)

    fig.add_traces([min_curve, max_curve, avg_curve], rows=1, cols=2)
    fig.add_trace(gr, 1, 1)
    fig.add_trace(map2d.data[0], row=1, col=4)

    # fig.update_yaxes(
    #     tickvals=np.linspace(0, len(time), 10),
    #     ticktext=np.round(np.linspace(time.min(), time.max(), 10), 2),
    #     autorange="reversed",
    #     row=1, col=3
    # )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    fig.update_yaxes(
        tickvals=np.linspace(0, len(data.index) - 1, 10),
        ticktext=np.round(np.linspace(data.index.min(), data.index.max(), 10), 2),
        autorange="reversed",
        row=1, col=1
    )

    fig.update_layout(
        coloraxis=dict(colorscale='Turbo'),
        hovermode='closest',
        yaxis=dict(autorange='reversed'),
        title='Well Integrity Tool Plot',
        yaxis_title='Depth',
        height=height,
        width=width,
        template=plotly_template,
                font=dict(family="Arial, sans-serif", size=9),
                legend=dict(x=1.01, y=1, traceorder='normal'),
                margin=dict(r=110,t=40),
                coloraxis_colorbar=dict(x=1, y=0.5, len=0.6)
    )

    for axis_name in fig.layout:
        if axis_name.startswith('xaxis') or axis_name.startswith('yaxis'):
            axis = fig.layout[axis_name]
            axis.showspikes = True
            axis.spikecolor = 'grey'
            axis.spikethickness = 1
            axis.spikesnap = 'cursor'
            axis.spikemode = 'across+marker'
            axis.spikedash = 'solid'

    return fig
def plot_3d_window(las_file_as_df: pd.DataFrame, fingers: list):

    # Read LAS data
    data = las_file_as_df
    fing = fingers

    trace_matrix = data[fing].to_numpy().T
    trace_matrix = trace_matrix.T
    
    # Tube parameters
    depth_len, angle_len = trace_matrix.shape
    theta = np.linspace(0, 2 * np.pi, angle_len)
    z_vals = np.linspace(0, 10, depth_len)
    theta_grid, z_grid = np.meshgrid(theta, z_vals)

    R = 1.0
    initial_alpha = 2
    initial_z_scale = 10

    # Function to regenerate geometry
    def update_tube(z_scale=None, alpha_scale=None):
        z_scale = z_scale if z_scale is not None else update_tube.z_scale
        alpha_scale = alpha_scale if alpha_scale is not None else update_tube.alpha

        radius = R + alpha_scale * trace_matrix
        X = radius * np.cos(theta_grid)
        Y = radius * np.sin(theta_grid)
        Z = z_grid * z_scale

        new_points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
        grid.points = new_points
        plotter.update()
        plotter.render()

        update_tube.z_scale = z_scale
        update_tube.alpha = alpha_scale

    # Store initial values
    update_tube.z_scale = initial_z_scale
    update_tube.alpha = initial_alpha

    # Initial mesh
    radius = R + initial_alpha * trace_matrix
    X = radius * np.cos(theta_grid)
    Y = radius * np.sin(theta_grid)
    Z = z_grid * initial_z_scale

    points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = [angle_len, depth_len, 1]
    grid["amplitude"] = trace_matrix.ravel()

    # Plotter
    plotter = pv.Plotter()
    plotter.add_mesh(grid, scalars="amplitude", cmap="turbo", show_edges=False)

    # Add Z (vertical) exaggeration slider
    plotter.add_slider_widget(
        callback=lambda val: update_tube(z_scale=val),
        rng=[1, 50],
        value=initial_z_scale,
        title='Z Scale',
        pointa=(0.02, 0.05),
        pointb=(0.15, 0.05),
        style='classic',
        title_height=0.015,
        slider_width=0.015,
        tube_width=0.003
    )

    # Add alpha (radial) exaggeration slider
    plotter.add_slider_widget(
        callback=lambda val: update_tube(alpha_scale=val),
        rng=[0.1, 5.0],
        value=initial_alpha,
        title='Radial Scale',
        pointa=(0.18, 0.05),
        pointb=(0.31, 0.05),
        style='classic',
        title_height=0.015,
        slider_width=0.015,
        tube_width=0.003
    )

    # Show the interactive window
    plotter.show()
def plot_3d_boundary_window(las_file_as_df: pd.DataFrame, fingers: list,
                              tubular_id=2.5, 
                              tubular_od=3):

    # Read LAS data
    data = las_file_as_df
    fing = fingers

    trace_matrix = data[fing].to_numpy().T
    trace_matrix = trace_matrix.T
    
    # Tube parameters
    depth_len, angle_len = trace_matrix.shape
    theta = np.linspace(0, 2 * np.pi, angle_len)
    z_vals = np.linspace(0, 10, depth_len)
    theta_grid, z_grid = np.meshgrid(theta, z_vals)

    R = 0
    initial_alpha = 1
    initial_z_scale = 10

    # Initial mesh
    radius = R + initial_alpha * trace_matrix
    X = radius * np.cos(theta_grid)
    Y = radius * np.sin(theta_grid)
    Z = z_grid * initial_z_scale

    points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    print(X.ravel())
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = [angle_len, depth_len, 1]
    grid["amplitude"] = trace_matrix.ravel()

    # Plotter
    plotter = pv.Plotter()
    plotter.add_mesh(grid, scalars="amplitude", cmap="turbo", show_edges=False)

    # Hollow cylinder setup
    tub_height = Z.max() - Z.min()

    shell_outer = make_cylinder_shell(radius=tubular_od/2, height=tub_height, thickness=0)
    shell_inner = make_cylinder_shell(radius=tubular_id/2, height=tub_height, thickness=0)
    plotter.add_mesh(shell_outer, color="black", opacity=.0, show_edges=False)

    plotter.add_mesh(shell_inner, color="red", opacity=0.0, show_edges=False)
    outer_actor = plotter.add_mesh(shell_outer, color='blue', opacity=1)

    # Add inner shell mesh, keep the actor
    inner_actor = plotter.add_mesh(shell_inner, color='red', opacity=1)
    def toggle_outer(checked):
        outer_actor.SetVisibility(checked)
        plotter.render()

    def toggle_inner(checked):
        inner_actor.SetVisibility(checked)
        plotter.render()

    # Add checkboxes
    plotter.add_checkbox_button_widget(toggle_outer, value=True, position=(10, 10), size=25)
    plotter.add_checkbox_button_widget(toggle_inner, value=True, position=(10, 50), size=25)
    # Show plot
    plotter.show(auto_close=False, interactive=True)

def plot_3d_patches_window(las_file_as_df: pd.DataFrame, fingers: list,
                              tubular_id=2.5, 
                              tubular_od=3):

    # Read LAS data
    data = las_file_as_df
    fing = fingers

    trace_matrix = data[fing].to_numpy().T
    trace_matrix = trace_matrix.T
    
    # Tube parameters
    depth_len, angle_len = trace_matrix.shape
    theta = np.linspace(0, 2 * np.pi, angle_len)
    z_vals = np.linspace(0, 10, depth_len)
    theta_grid, z_grid = np.meshgrid(theta, z_vals)

    R = 0
    initial_alpha = 1
    initial_z_scale = 10

    # Initial mesh
    radius = R + initial_alpha * trace_matrix
    X = radius * np.cos(theta_grid)
    Y = radius * np.sin(theta_grid)
    Z = z_grid * initial_z_scale

    points = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
    print(X.ravel())
    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = [angle_len, depth_len, 1]
    grid["amplitude"] = trace_matrix.ravel()

    # Plotter
    plotter = pv.Plotter()
    #plotter.add_mesh(grid, scalars="amplitude", cmap="turbo", show_edges=False)

    # Hollow cylinder setup
    tub_height = Z.max() - Z.min()

    shell_outer = make_cylinder_shell(radius=tubular_od/2, height=tub_height, thickness=0)
    shell_inner = make_cylinder_shell(radius=tubular_id/2, height=tub_height, thickness=0)
    #plotter.add_mesh(shell_outer, color="black", opacity=.0, show_edges=False)
    grid_surf = grid.extract_surface().triangulate().clean()
    shell_surf = shell_inner.extract_surface().triangulate().clean()

    #subtract = grid_surf.boolean_intersection(shell_surf)
    plotter.add_mesh(shell_inner, color="red", opacity=0.0, show_edges=False)
    mask = radius > (tubular_id/2)
    masked_amplitude = np.where(mask, trace_matrix, np.nan)

    masked_grid = pv.StructuredGrid()
    masked_grid.points = points
    masked_grid.dimensions = [angle_len, depth_len, 1]
    masked_grid["amplitude"] = masked_amplitude.ravel(order='C')

    # Plot only masked parts
    plotter.add_mesh(masked_grid, scalars="amplitude", cmap="turbo", show_edges=False, nan_opacity=0.0)
    plotter.show( auto_close=False, interactive=True)

def make_cylinder_shell(radius=1.0, height=10.0, thickness=0.05, theta_res=100, z_res=200):
    theta = np.linspace(0, 2 * np.pi, theta_res)
    z = np.linspace(0, height, z_res)
    theta_grid, z_grid = np.meshgrid(theta, z)

    r = radius + thickness  # shell sits just outside radius
    X = r * np.cos(theta_grid)
    Y = r * np.sin(theta_grid)
    Z = z_grid

    # Reshape to match PyVista's expected order: [z_res, theta_res]
    X = X.reshape((z_res, theta_res))
    Y = Y.reshape((z_res, theta_res))
    Z = Z.reshape((z_res, theta_res))

    shell = pv.StructuredGrid(X, Y, Z)
    return shell