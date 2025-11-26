
#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import argparse

def convert_inertial(sdf_inertial, urdf_link):
    inertial = ET.SubElement(urdf_link, "inertial")

    mass_tag = sdf_inertial.find("mass")
    if mass_tag is not None:
        mass = ET.SubElement(inertial, "mass")
        mass.set("value", mass_tag.text)

    inertia_tag = sdf_inertial.find("inertia")
    if inertia_tag is not None:
        inertia = ET.SubElement(inertial, "inertia")
        for key in ["ixx", "iyy", "izz", "ixy", "ixz", "iyz"]:
            child = inertia_tag.find(key)
            if child is not None:
                inertia.set(key, child.text)


def convert_geometry(sdf_geom, parent):
    geom = ET.SubElement(parent, "geometry")

    if sdf_geom.find("mesh") is not None:
        mesh_sdf = sdf_geom.find("mesh")
        mesh = ET.SubElement(geom, "mesh")

        uri = mesh_sdf.find("uri")
        if uri is not None:
            mesh.set("filename", uri.text)

        scale = mesh_sdf.find("scale")
        if scale is not None:
            mesh.set("scale", scale.text)

    elif sdf_geom.find("box") is not None:
        size = sdf_geom.find("box").find("size")
        box = ET.SubElement(geom, "box")
        box.set("size", size.text)

    elif sdf_geom.find("cylinder") is not None:
        cyl = sdf_geom.find("cylinder")
        cylinder = ET.SubElement(geom, "cylinder")
        cylinder.set("radius", cyl.find("radius").text)
        cylinder.set("length", cyl.find("length").text)

    elif sdf_geom.find("sphere") is not None:
        sphere = ET.SubElement(geom, "sphere")
        sphere.set("radius", sdf_geom.find("sphere").find("radius").text)


def convert_pose(sdf_pose, parent):
    if sdf_pose is None:
        origin = ET.SubElement(parent, "origin")
        origin.set("xyz", "0 0 0")
        origin.set("rpy", "0 0 0")
        return

    vals = sdf_pose.text.split()
    xyz = " ".join(vals[0:3])
    rpy = " ".join(vals[3:6])

    origin = ET.SubElement(parent, "origin")
    origin.set("xyz", xyz)
    origin.set("rpy", rpy)


def sdf_to_urdf(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    robot = ET.Element("robot")
    robot.set("name", root.attrib.get("name", "converted_robot"))

    # Convert each link
    for sdf_link in root.findall(".//link"):
        link = ET.SubElement(robot, "link")
        link.set("name", sdf_link.attrib["name"])

        # Inertial
        if sdf_link.find("inertial") is not None:
            convert_inertial(sdf_link.find("inertial"), link)

        # Visual
        for sdf_vis in sdf_link.findall("visual"):
            visual = ET.SubElement(link, "visual")
            convert_pose(sdf_vis.find("pose"), visual)
            convert_geometry(sdf_vis.find("geometry"), visual)

        # Collision
        for sdf_col in sdf_link.findall("collision"):
            collision = ET.SubElement(link, "collision")
            convert_pose(sdf_col.find("pose"), collision)
            convert_geometry(sdf_col.find("geometry"), collision)

    # Convert joints
    for sdf_joint in root.findall(".//joint"):
        joint = ET.SubElement(robot, "joint")
        joint.set("name", sdf_joint.attrib["name"])
        joint.set("type", sdf_joint.attrib.get("type", "fixed"))

        parent_link = sdf_joint.find("parent").text
        child_link = sdf_joint.find("child").text

        parent = ET.SubElement(joint, "parent")
        parent.set("link", parent_link)
        child = ET.SubElement(joint, "child")
        child.set("link", child_link)

        convert_pose(sdf_joint.find("pose"), joint)

    # Save
    ET.indent(robot)
    with open(output_file, "w") as f:
        f.write(ET.tostring(robot).decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sdf", help="Input SDF file")
    parser.add_argument("urdf", help="Output URDF file")
    args = parser.parse_args()

    sdf_to_urdf(args.sdf, args.urdf)
    print(f"✓ Converted {args.sdf} → {args.urdf}")
