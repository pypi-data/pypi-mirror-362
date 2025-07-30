import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from IPython.display import display, HTML
import os
from typing import Optional
import ipywidgets as widgets
from IPython.display import display, clear_output

class VisLotan:
    @staticmethod
    def plt_plot(df, events, plot_by='index', figsize=(16, 10)):
        """
        Generates line plots for the specified events in the dataframe using matplotlib.

        Parameters:
        - df (DataFrame): The Pandas DataFrame containing the data.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - figsize (tuple): The size of the figure (width, height) in inches.

        Returns:
        None. Displays the plot inline.
        """
        fig, axs = plt.subplots(len(events), figsize=figsize)

        x = df.index if plot_by == 'index' else df[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                axs[i].plot(x, df[event], label=event)
                axs[i].legend(loc='lower right')

    @staticmethod
    def plotly_plot(df, events, plot_by='index', mode='lines', height=800, width=1600):
        """
        Generates interactive line plots for the specified events in the dataframe using Plotly.

        Parameters:
        - df (DataFrame): The Pandas DataFrame containing the data.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - mode (str): The drawing mode for the plot ('lines', 'markers', 'lines+markers', etc.).

        Returns:
        fig (Figure): A Plotly Figure object that can be displayed or further customized.
        """
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        x = df.index if plot_by == 'index' else df[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(
                    go.Scatter(
                        x=x, y=df[event], name=event, mode=mode,
                        marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )

                # Annotation example, can be customized or removed
                fig.add_annotation(
                    text="text",
                    xref="paper", yref="paper",
                    x=1.2, y=0.6,
                    showarrow=False,
                    align='left'
                )

        fig.update_layout(showlegend=True, height=height, width=width)

        return fig

    @staticmethod
    def plotly_plot_2df(df1, df2, events, plot_by='index', label1='1st', label2='2nd',
                        mode1='lines', mode2= 'markers', title="", height=800, width=1600):
        """
        Generates interactive line plots for the specified events, comparing two dataframes using Plotly.

        Parameters:
        - df1, df2 (DataFrame): The Pandas DataFrames containing the data to compare.
        - events (list of list): A list of event group lists. Each event group will be plotted in a separate subplot.
        - plot_by (str): Column name to use for the x-axis. If 'index', the DataFrame's index will be used.
        - label1, label2 (str): Labels for the data series from df1 and df2 respectively.
        - title (str): The title of the plot.

        Returns:
        fig (Figure): A Plotly Figure object that can be displayed or further customized.
        """
        fig = make_subplots(rows=len(events), cols=1, shared_xaxes=True, vertical_spacing=0.05)

        x1 = df1.index if plot_by == 'index' else df1[plot_by]
        x2 = df2.index if plot_by == 'index' else df2[plot_by]

        for i, event_group in enumerate(events):
            for event in event_group:
                fig.add_trace(
                    go.Scatter(
                        x=x1, y=df1[event], name=f"{label1} {event}",
                        mode=mode1, marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )
                fig.add_trace(
                    go.Scatter(
                        x=x2, y=df2[event], name=f"{label2} {event}",
                        mode=mode2, marker=dict(size=6, line=dict(width=2))
                    ),
                    row=i + 1, col=1, secondary_y=False
                )

                # Annotation example, can be customized or removed
                fig.add_annotation(
                    text="text",
                    xref="paper", yref="paper",
                    x=1.2, y=0.6,
                    showarrow=False,
                    align='left'
                )

        fig.update_layout(showlegend=True, height=height, width=width, title=title)

        return fig

    @staticmethod
    def set_width(size):
        """
        Sets the width of the Jupyter Notebook container and the maximum number of displayed rows.

        Parameters:
        - size (int): The desired width percentage of the container and the maximum number of rows to display.

        Returns:
        None. Adjusts the notebook display settings.
        """
        display(HTML(f"<style>.container {{ width:{size}% !important; }}</style>"))
        pd.set_option('display.max_rows', size)



    def select_folder(base_path: str) -> Optional[str]:
        """
        Display a dropdown of folders from the specified base path,
        and return the folder selected by the user.

        Parameters:
            base_path (str): The directory path to list folders from.

        Returns:
            Optional[str]: The name of the selected folder, or None if no selection is made.
        """
        # Get list of folders, sorted reverse alphabetically
        folders = sorted(
            [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))],
            reverse=True
        )

        if not folders:
            raise ValueError("No folders found in the specified path. Try picking a less empty place!")

        # UI Elements
        folder_dropdown = widgets.Dropdown(
            options=folders,
            description='Folder:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        confirm_button = widgets.Button(description="Confirm Selection", button_style='success')
        output = widgets.Output()
        selected_folder = {}

        def on_confirm_clicked(_):
            selected = folder_dropdown.value
            selected_folder['value'] = selected
            with output:
                clear_output()
                print(f"✅ Selected folder: {selected}")

        # Display the UI
        display(widgets.VBox([
            widgets.HTML("<b>Select a folder:</b>"),
            folder_dropdown,
            confirm_button,
            output
        ]))

        confirm_button.on_click(on_confirm_clicked)

        # Return value is stored in selected_folder['value']
        return selected_folder


    def select_file(base_path: str) -> Optional[dict]:
        """
        Display a dropdown of files from the specified base path,
        and return the file selected by the user.

        Parameters:
            base_path (str): The directory path to list files from.

        Returns:
            Optional[dict]: A dictionary with key 'value' containing the selected file name,
                            or empty if no file is selected yet.
        """
        # Get list of files, sorted reverse alphabetically
        files = sorted(
            [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))],
            reverse=True
        )

        if not files:
            raise ValueError("No files found in the specified path. Try picking a place with actual files!")

        # UI Elements
        file_dropdown = widgets.Dropdown(
            options=files,
            description='File:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='50%')
        )

        confirm_button = widgets.Button(description="Confirm Selection", button_style='info')
        output = widgets.Output()
        selected_file = {}

        def on_confirm_clicked(_):
            selected = file_dropdown.value
            selected_file['value'] = selected
            with output:
                clear_output()
                print(f"📄 Selected file: {selected}")

        # Display the UI
        display(widgets.VBox([
            widgets.HTML("<b>Select a file:</b>"),
            file_dropdown,
            confirm_button,
            output
        ]))

        confirm_button.on_click(on_confirm_clicked)

        # Return a dictionary with selection (poll externally for 'value')
        return selected_file # This requires polling externally to check if selection is done