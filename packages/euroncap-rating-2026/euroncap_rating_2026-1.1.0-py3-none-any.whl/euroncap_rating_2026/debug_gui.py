import tkinter as tk
from tkinter import ttk


def show_criteria(sheet_dict):
    """
    Displays the criteria values in a Tkinter GUI.

    Args:
        sheet_dict (dict): A dictionary where the keys are sheet names and the values are lists of LoadCase objects.
    """
    print("-" * 40)
    print("Showing criteria values in GUI")
    print("Exit GUI to continue")
    print("-" * 40)
    root = tk.Tk()
    root.title("NCAP Debug GUI")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill="both")

    def create_treeview(tab, load_cases):
        """
        Creates a Treeview widget to display the criteria values.

        Args:
            tab (ttk.Frame): The tab in which the Treeview will be created.
            load_cases (list): A list of LoadCase objects to be displayed.
        """
        tree = ttk.Treeview(tab)
        tree["columns"] = (
            "Load Case ID",
            "Load Case",
            "Seat",
            "Dummy",
            "Body Region",
            "Criteria",
            "Criteria Type",
            "Value",
            "HPL",
            "LPL",
            "Color",
            "Score",
            "Test Point",
            "OEM.Prediction",
            "Prediction.Check",
            "BodyRegion Score",
            "BodyRegion Attribute Score",
            "Score inspection",
            "Max Score",
            "Dummy Score",
            "Dummy Max Score",
        )
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Load Case ID", anchor=tk.W, width=80)
        tree.column("Load Case", anchor=tk.W, width=120)
        tree.column("Seat", anchor=tk.W, width=120)
        tree.column("Dummy", anchor=tk.W, width=120)
        tree.column("Body Region", anchor=tk.W, width=120)
        tree.column("Criteria", anchor=tk.W, width=120)
        tree.column("Criteria Type", anchor=tk.W, width=120)
        tree.column("Value", anchor=tk.W, width=120)
        tree.column("HPL", anchor=tk.W, width=120)
        tree.column("LPL", anchor=tk.W, width=120)
        tree.column("Color", anchor=tk.W, width=120)
        tree.column("Score", anchor=tk.W, width=120)
        tree.column("Test Point", anchor=tk.W, width=120)
        tree.column("OEM.Prediction", anchor=tk.W, width=120)
        tree.column("Prediction.Check", anchor=tk.W, width=120)
        tree.column("BodyRegion Score", anchor=tk.W, width=120)
        tree.column("BodyRegion Attribute Score", anchor=tk.W, width=120)
        tree.column("Score inspection", anchor=tk.W, width=120)
        tree.column("Max Score", anchor=tk.W, width=120)
        tree.column("Dummy Score", anchor=tk.W, width=120)
        tree.column("Dummy Max Score", anchor=tk.W, width=120)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Load Case ID", text="Load Case ID", anchor=tk.W)
        tree.heading("Load Case", text="Load Case", anchor=tk.W)
        tree.heading("Seat", text="Seat", anchor=tk.W)
        tree.heading("Dummy", text="Dummy", anchor=tk.W)
        tree.heading("Body Region", text="Body Region", anchor=tk.W)
        tree.heading("Criteria", text="Criteria", anchor=tk.W)
        tree.heading("Criteria Type", text="Criteria Type", anchor=tk.W)
        tree.heading("Value", text="Value", anchor=tk.W)
        tree.heading("HPL", text="HPL", anchor=tk.W)
        tree.heading("LPL", text="LPL", anchor=tk.W)
        tree.heading("Color", text="Color", anchor=tk.W)
        tree.heading("Score", text="Score", anchor=tk.W)
        tree.heading("Test Point", text="Test Point", anchor=tk.W)
        tree.heading("OEM.Prediction", text="OEM.Prediction", anchor=tk.W)
        tree.heading("Prediction.Check", text="Prediction.Check", anchor=tk.W)
        tree.heading("BodyRegion Score", text="BodyRegion Score", anchor=tk.W)
        tree.heading(
            "BodyRegion Attribute Score", text="BodyRegion Attribute Score", anchor=tk.W
        )
        tree.heading("Score inspection", text="Score inspection", anchor=tk.W)
        tree.heading("Max Score", text="Max Score", anchor=tk.W)
        tree.heading("Dummy Score", text="Dummy Score", anchor=tk.W)
        tree.heading("Dummy Max Score", text="Dummy Max Score", anchor=tk.W)

        previous_values = {
            "load_case": None,
            "seat": None,
            "dummy": None,
            "body_region": None,
        }

        def insert_body_region(tree, load_case, seat, dummy, body_region):
            """
            Inserts a body region's criteria into the Treeview.

            Args:
                tree (ttk.Treeview): The Treeview widget.
                load_case (LoadCase): The load case object.
                seat (Seat): The seat object.
                dummy (Dummy): The dummy object.
                body_region (BodyRegion): The body region object.
            """
            for criteria in body_region._criteria:
                load_case_id = load_case.id
                load_case_name = (
                    load_case.name
                    if previous_values["load_case"] != load_case.name
                    else ""
                )
                seat_name = seat.name if previous_values["seat"] != seat.name else ""
                dummy_name = (
                    dummy.name if previous_values["dummy"] != dummy.name else ""
                )
                body_region_name = (
                    body_region.name
                    if previous_values["body_region"] != body_region.name
                    else ""
                )

                tree.insert(
                    "",
                    "end",
                    values=(
                        load_case_id,
                        load_case_name,
                        seat_name,
                        dummy_name,
                        body_region_name,
                        criteria.name,
                        criteria.criteria_type,  # Added criteria_type column
                        criteria.value,
                        criteria.hpl,
                        criteria.lpl,
                        criteria.color,
                        criteria.score,
                        criteria.test_point,
                        criteria.prediction,
                        criteria.prediction_result,
                        body_region.score,
                        body_region.bodyregion_score,
                        body_region.inspection,
                        body_region.max_score,
                        dummy.score,
                        dummy.max_score,
                    ),
                )

                previous_values.update(
                    {
                        "load_case": load_case.name,
                        "seat": seat.name,
                        "dummy": dummy.name,
                        "body_region": body_region.name,
                    }
                )

        for load_case in load_cases:
            for seat in load_case.seats:
                dummy = seat.dummy
                for body_region in dummy.body_region_list:
                    insert_body_region(tree, load_case, seat, dummy, body_region)

        tree.pack(pady=120)

    for sheet_name, load_cases in sheet_dict.items():
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=sheet_name)
        create_treeview(tab, load_cases)

    root.mainloop()
