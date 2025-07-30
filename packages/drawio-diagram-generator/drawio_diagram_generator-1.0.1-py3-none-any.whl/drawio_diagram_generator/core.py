import uuid
import html
import urllib.request
from PIL import Image
import io


def build_style_string(**kwargs):
    """Helper to build a Draw.io style string from key-value pairs."""
    return ";".join(f"{k}={v}" for k, v in kwargs.items()) + ";"


class DiagramComponent:
    """Base class for all diagram components."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.parent_id = "1"

    def _calculate_layout(self, x=0, y=0):
        raise NotImplementedError

    def _render_to_cells(self):
        raise NotImplementedError

    def _set_parent_id(self, parent_id):
        """Recursively set the parent ID for a component and all its descendants."""
        self.parent_id = parent_id
        # Handle components that have a list of children (Row, Column, Group)
        if hasattr(self, "children"):
            for child in self.children:
                child._set_parent_id(parent_id)
        # Handle components that have a single child (legacy or specific use)
        elif hasattr(self, "child"):
            self.child._set_parent_id(parent_id)

        # Also set parent for other components like arrows within a group
        if hasattr(self, "other_components"):
            for component in self.other_components:
                component._set_parent_id(parent_id)


class Box(DiagramComponent):
    """A primitive component representing a single rectangle with text and optional icon or image-only mode."""

    def __init__(self, label, width=80, height=80, style=None, image_url=None, image_only=False):
        super().__init__()
        self.label = html.escape(label)
        self.width = width
        self.height = height
        self.image_url = image_url
        self.image_only = image_only
        if image_only and image_url:
            # Only show the image, no label, no box
            self.style = f"shape=image;image={image_url};"
            self.label = ""
        elif image_url:
            # Use label shape with image on the left
            base_style = "shape=label;imageAlign=left;imageWidth=24;imageHeight=24;"
            if style:
                base_style += style
            self.style = f"{base_style}image={image_url};"
        else:
            self.style = (
                style
                or "rounded=1;whiteSpace=wrap;html=1;shadow=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontColor=#000000;"
            )

    def _calculate_layout(self, x=0, y=0):
        self.x = x
        self.y = y

    def _render_to_cells(self):
        return [
            f"""
        <mxCell id="{self.id}" value="{self.label}" style="{self.style}" vertex="1" parent="{self.parent_id}">
            <mxGeometry x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" as="geometry" />
        </mxCell>"""
        ]


class IconBox(DiagramComponent):
    def __init__(self, image_url, width=80, height=80, style=None):
        super().__init__()
        self.image_url = image_url
        self.width = width
        self.height = height
        self.style = f"shape=image;image={image_url};"

    def _calculate_layout(self, x=0, y=0):
        self.x = x
        self.y = y

    def _render_to_cells(self):
        return [
            f"""
        <mxCell id=\"{self.id}\" value=\"\" style=\"{self.style}\" vertex=\"1\" parent=\"{self.parent_id}\">
            <mxGeometry x=\"{self.x}\" y=\"{self.y}\" width=\"{self.width}\" height=\"{self.height}\" as=\"geometry\" />
        </mxCell>"""
        ]


class Arrow(DiagramComponent):
    """A component representing a connection between two other components, with direction control."""

    def __init__(self, source, target, label="", style=None, direction="LR", show_arrow=True):
        super().__init__()
        self.source_id = source.id if isinstance(source, DiagramComponent) else source
        self.target_id = target.id if isinstance(target, DiagramComponent) else target
        self.label = html.escape(label)
        self.direction = direction
        self.show_arrow = show_arrow
        # Directional style
        direction_map = {
            "LR": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
            "RL": "exitX=0;exitY=0.5;entryX=1;entryY=0.5;",
            "TB": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
            "BT": "exitX=0.5;exitY=0;entryX=0.5;entryY=1;",
            "TT": "exitX=0.5;exitY=0;entryX=0.5;entryY=0;",
            "BB": "exitX=0.5;exitY=1;entryX=0.5;entryY=1;",
            "LL": "exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
            "RR": "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
            # Các hướng chéo:
            "RT": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;",   # phải sang trên
            "TR": "exitX=0.5;exitY=0;entryX=1;entryY=0.5;",   # trên sang phải
            "RB": "exitX=1;exitY=0.5;entryX=0.5;entryY=1;",   # phải sang dưới
            "BR": "exitX=0.5;exitY=1;entryX=1;entryY=0.5;",   # dưới sang phải
            "LT": "exitX=0;exitY=0.5;entryX=0.5;entryY=0;",   # trái sang trên
            "TL": "exitX=0.5;exitY=0;entryX=0;entryY=0.5;",   # trên sang trái
            "LB": "exitX=0;exitY=0.5;entryX=0.5;entryY=1;",   # trái sang dưới
            "BL": "exitX=0.5;exitY=1;entryX=0;entryY=0.5;",   # dưới sang trái
        }
        dir_style = direction_map.get(direction, direction_map["LR"])
        base_style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#000000;fontColor=#000000;backgroundColor=#ffffff;"
        )
        if not show_arrow:
            base_style += "endArrow=none;"
        if style:
            base_style += style
        self.style = f"{base_style}{dir_style}"

    def _calculate_layout(self, x=0, y=0):
        pass

    def _render_to_cells(self):
        return [
            f"""
        <mxCell id="{self.id}" value="{self.label}" style="{self.style}" edge="1" parent="{self.parent_id}" source="{self.source_id}" target="{self.target_id}">
            <mxGeometry relative="1" as="geometry" />
        </mxCell>"""
        ]


class Line(DiagramComponent):
    """A component representing a simple line connection without arrows between two components."""

    def __init__(self, source, target, label="", style=None, direction="LR"):
        super().__init__()
        self.source_id = source.id if isinstance(source, DiagramComponent) else source
        self.target_id = target.id if isinstance(target, DiagramComponent) else target
        self.label = html.escape(label)
        self.direction = direction
        # Directional style
        direction_map = {
            "LR": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;",
            "RL": "exitX=0;exitY=0.5;entryX=1;entryY=0.5;",
            "TB": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;",
            "BT": "exitX=0.5;exitY=0;entryX=0.5;entryY=1;",
            "TT": "exitX=0.5;exitY=0;entryX=0.5;entryY=0;",
            "BB": "exitX=0.5;exitY=1;entryX=0.5;entryY=1;",
            "LL": "exitX=0;exitY=0.5;entryX=0;entryY=0.5;",
            "RR": "exitX=1;exitY=0.5;entryX=1;entryY=0.5;",
            # Các hướng chéo:
            "RT": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;",   # phải sang trên
            "TR": "exitX=0.5;exitY=0;entryX=1;entryY=0.5;",   # trên sang phải
            "RB": "exitX=1;exitY=0.5;entryX=0.5;entryY=1;",   # phải sang dưới
            "BR": "exitX=0.5;exitY=1;entryX=1;entryY=0.5;",   # dưới sang phải
            "LT": "exitX=0;exitY=0.5;entryX=0.5;entryY=0;",   # trái sang trên
            "TL": "exitX=0.5;exitY=0;entryX=0;entryY=0.5;",   # trên sang trái
            "LB": "exitX=0;exitY=0.5;entryX=0.5;entryY=1;",   # trái sang dưới
            "BL": "exitX=0.5;exitY=1;entryX=0;entryY=0.5;",   # dưới sang trái
        }
        dir_style = direction_map.get(direction, direction_map["LR"])
        base_style = (
            "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
            "strokeColor=#000000;fontColor=#000000;backgroundColor=#ffffff;endArrow=none;"
        )
        if style:
            base_style += style
        self.style = f"{base_style}{dir_style}"

    def _calculate_layout(self, x=0, y=0):
        pass

    def _render_to_cells(self):
        return [
            f"""
        <mxCell id="{self.id}" value="{self.label}" style="{self.style}" edge="1" parent="{self.parent_id}" source="{self.source_id}" target="{self.target_id}">
            <mxGeometry relative="1" as="geometry" />
        </mxCell>"""
        ]


class Column(DiagramComponent):
    """A layout component that arranges its children vertically."""

    def __init__(self, children, spacing=40, align="center"):
        super().__init__()
        self.children = children
        self.spacing = spacing
        if align not in ["left", "center", "right"]:
            raise ValueError("Align must be 'left', 'center', or 'right'")
        self.align = align

    def _calculate_layout(self, x=0, y=0):
        self.x, self.y = x, y
        max_child_width = 0
        for child in self.children:
            child._calculate_layout()
            if child.width > max_child_width:
                max_child_width = child.width
        self.width = max_child_width

        current_y = y
        for child in self.children:
            child_x = x
            if self.align == "center":
                child_x = x + (self.width - child.width) / 2
            elif self.align == "right":
                child_x = x + (self.width - child.width)
            child._calculate_layout(child_x, current_y)
            current_y += child.height + self.spacing

        self.height = (current_y - y - self.spacing) if self.children else 0

    def _render_to_cells(self):
        all_cells = []
        for child in self.children:
            all_cells.extend(child._render_to_cells())
        return all_cells


class Row(DiagramComponent):
    """A layout component that arranges its children horizontally."""

    def __init__(self, children, spacing=50, align="middle"):
        super().__init__()
        self.children = children
        self.spacing = spacing
        if align not in ["top", "middle", "bottom"]:
            raise ValueError("Align must be 'top', 'middle', or 'bottom'")
        self.align = align

    def _calculate_layout(self, x=0, y=0):
        self.x, self.y = x, y
        max_child_height = 0
        for child in self.children:
            child._calculate_layout()
            if child.height > max_child_height:
                max_child_height = child.height
        self.height = max_child_height

        current_x = x
        for child in self.children:
            child_y = y
            if self.align == "middle":
                child_y = y + (self.height - child.height) / 2
            elif self.align == "bottom":
                child_y = y + (self.height - child.height)
            child._calculate_layout(current_x, child_y)
            current_x += child.width + self.spacing

        self.width = (current_x - x - self.spacing) if self.children else 0

    def _render_to_cells(self):
        all_cells = []
        for child in self.children:
            all_cells.extend(child._render_to_cells())
        return all_cells


class Group(DiagramComponent):
    """
    A container that visually groups multiple children, arranging them
    automatically in a row or column.
    """

    def __init__(
        self,
        label,
        children,
        layout="column",
        align="center",
        spacing=50,
        padding=50,
        other_components=None,
        style_opts=None,
        is_root=False,
    ):
        super().__init__()
        self.label = html.escape(label)
        self.children = children
        self.other_components = other_components or []
        self.padding = padding

        # Internally use a Row or Column to manage the layout of children
        if layout == "column":
            self.layout_manager = Column(children, spacing=spacing, align=align)
        elif layout == "row":
            self.layout_manager = Row(children, spacing=spacing, align=align)
        else:
            raise ValueError("Layout must be 'column' or 'row'")

        # Set default styles
        default_style = {
            "shape": "mxgraph.aws4.group",
            "container": 1,
            "collapsible": 0,
            "recursiveResize": 0,
            "verticalAlign": "top",
            "align": "left",
            "spacingLeft": 30,
            "grIcon": "mxgraph.aws4.group_aws_cloud_alt",
            "strokeColor": "#232F3E",
            "fillColor": "none",
            "fontColor": "#232F3E",
        }
        if style_opts:
            default_style.update(style_opts)
        self.style = build_style_string(**default_style)

        # Sửa logic set parent_id cho root group
        if is_root:
            self._set_parent_id("1")
        else:
            self._set_parent_id(self.id)

    def _calculate_layout(self, x=0, y=0):
        self.x, self.y = x, y

        # Delegate layout calculation to the internal layout manager
        self.layout_manager._calculate_layout(x + self.padding, y + self.padding)

        # Group's size is the layout's size plus padding
        self.width = self.layout_manager.width + 2 * self.padding
        self.height = self.layout_manager.height + 2 * self.padding

        for component in self.other_components:
            component._calculate_layout()

    def _render_to_cells(self):
        group_cell = f"""
        <mxCell id="{self.id}" value="{self.label}" style="{self.style}" vertex="1" parent="{self.parent_id}">
            <mxGeometry x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" as="geometry" />
        </mxCell>"""

        all_cells = [group_cell]
        all_cells.extend(self.layout_manager._render_to_cells())
        for component in self.other_components:
            all_cells.extend(component._render_to_cells())
        return all_cells


class Diagram:
    """The main class that orchestrates the entire process."""

    def __init__(self, root_component):
        self.root_component = root_component

    def to_xml(self, dx=20, dy=20):
        self.root_component._calculate_layout(dx, dy)
        cells = self.root_component._render_to_cells()
        cells_xml = "".join(cells)
        return f"""<mxfile host="Electron" modified="2025-07-04T00:00:00.000Z" agent="PythonDiagramGenerator" etag="UNIQUE_ETAG" version="21.0.0" type="device">
    <diagram name="Page-1" id="UNIQUE_PAGE_ID">
        <mxGraphModel dx="1434" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
            <root>
                <mxCell id="0" />
                <mxCell id="1" parent="0" />
                {cells_xml}
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>"""

    def save(self, file_path, dx=20, dy=20):
        """
        Save the diagram to a file.
        
        Args:
            file_path (str): Path to the output file
            dx (int): X offset for layout
            dy (int): Y offset for layout
        """
        save_diagram_to_file(self, file_path)


def save_diagram_to_file(diagram, file_path):
    """
    Chuyển diagram thành XML và lưu vào file.
    """
    xml_content = diagram.to_xml()
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xml_content)


# --- Example Usage ---
if __name__ == "__main__":
    # --- Define Components for App Subnet ---
    api_gateway = Box("API Gateway", width=150)
    service_a = IconBox("https://i.ibb.co/9HCnrtmV/Screenshot-2025-07-04-200239.png")
    service_b = Box("Service B")
    service_c = Box("Service C")
    microservices_row = Row(children=[service_a, service_b, service_c], align="middle")
    app_core_layout = Column(children=[api_gateway, microservices_row], align="center")

    api1 = Box("API 1")
    service_a1 = Box("Service A1")
    service_b1 = Box("Service B1")
    service_c1 = Box("Service C1")
    microservices_row1 = Row(children=[service_a1, service_b1, service_c1], align="middle")
    app_core_layout1 = Column(children=[api1, microservices_row1], align="center")

    app_connections = [
        Arrow(api_gateway, service_a, direction="TB"),
        Arrow(api_gateway, service_b, direction="TB"),
        Arrow(service_b, service_c, label="Sends event", direction="LR"),
    ]

    app_connections1 = [
        Arrow(api1, service_a1, direction="TB"),
        Arrow(api1, service_b1, direction="TB"),
        Arrow(service_b1, service_c1, label="Sends event", direction="LR"),
    ]

    app_subnet = Group(
        label="App Subnet",
        children=[app_core_layout],  # Children must be a list
        other_components=app_connections,
        padding=40,
        style_opts={
            "grIcon": "mxgraph.aws4.group_security_group",
            "strokeColor": "#00A4A6",
            "fillColor": "#E6F6F7",
        },
    )

    app_subnet1 = Group(
        label="App Subnet",
        children=[app_core_layout1],  # Children must be a list
        other_components=app_connections1,
        padding=40,
    )

    # --- Define Components for DB Subnet ---
    main_db = Box("Main RDS Database", width=180, height=80)
    read_replica = Box("Read Replica", width=180, height=80)
    db_connections = [Arrow(main_db, read_replica, "Replication", direction="TB")]

    main_db2 = Box("Main RDS Database", width=180, height=80)
    read_replica2 = Box("Read Replica", width=180, height=80)
    db_connections2 = [Arrow(main_db, read_replica, "Replication", direction="TB")]

    db_subnet = Group(
        label="DB Subnet",
        children=[main_db, read_replica],
        layout="column",
        align="center",
        other_components=db_connections,
        padding=40,
        style_opts={
            "grIcon": "mxgraph.aws4.group_database",
            "strokeColor": "#D9A44E",
            "fillColor": "#FAF3E5",
        },
    )

    db_subnet2 = Group(
        label="DB Subnet2",
        children=[main_db2, read_replica2],
        layout="column",
        align="center",
        other_components=db_connections2,
        padding=40,
        style_opts={
            "grIcon": "mxgraph.aws4.group_database",
            "strokeColor": "#D9A44E",
            "fillColor": "#FAF3E5",
        },
    )

    # --- Define the VPC to contain the subnets ---
    # The key change: The VPC group now takes a LIST of children (the two subnets)
    # and arranges them in a row.
    vpc = Group(
        label="VPC (Virtual Private Cloud)",
        children=[app_subnet, db_subnet, db_subnet2, app_subnet1],  # Pass the two subnets as a list
        layout="row",  # Arrange them horizontally
        align="middle",  # Vertically align them to the middle
        spacing=40,  # Space between the subnets
        padding=40,
        # Connections between subnets can be defined here
        other_components=[Arrow(app_subnet, db_subnet, "Data Access")],
        style_opts={"grIcon": "mxgraph.aws4.group_vpc2", "strokeColor": "#8C4FFF"},
    )

    # --- Wrap everything in the top-level cloud ---
    aws_cloud = Group(
        label="AWS Cloud",
        children=[vpc],  # The VPC is the single child of the AWS cloud
        padding=40,
        style_opts={
            "grIcon": "mxgraph.aws4.group_aws_cloud_alt",
            "strokeColor": "#232F3E",
        },
        is_root=True,
    )

    # --- Generate the diagram ---
    diagram = Diagram(root_component=aws_cloud)
    xml_output = diagram.to_xml()
    file_path = "aws_multisubnet_architecture.drawio"
    with open(file_path, "w") as f:
        f.write(xml_output)

    print(f"Diagram successfully generated and saved to '{file_path}'")


    diagram = Diagram(root_component=aws_cloud)
    xml_output = diagram.to_xml()
    file_path = "aws_multisubnet_architecture.drawio"
    with open(file_path, "w") as f:
        f.write(xml_output)

    print(f"Diagram successfully generated and saved to '{file_path}'")

