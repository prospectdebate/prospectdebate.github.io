"""Build and render the Prospect gold-panther shard assembly in Blender.

Usage:
  blender --background --python tools/render_panther.py -- --preview
  blender --background --python tools/render_panther.py -- --animation
"""

import bpy
import math
import os
import random
import sys
from mathutils import Vector


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(ROOT, "assets", "video")
FRAME_DIR = os.path.join(VIDEO_DIR, "panther-shards-frames")
ARGS = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
PREVIEW = "--preview" in ARGS
ANIMATION = "--animation" in ARGS


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def material(name, color, metallic=0.0, roughness=0.45, emission=None):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 3.5
    return mat


def apply_transform(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    obj.select_set(False)


def ico(name, location, scale, rotation=(0, 0, 0), subdivisions=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    apply_transform(obj)
    return obj


def cone(name, location, radius1, radius2, depth, rotation=(0, 0, 0), vertices=5):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    apply_transform(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.quads_convert_to_tris(quad_method="BEAUTY", ngon_method="BEAUTY")
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def cylinder_between(name, start, end, radius_start, radius_end=None, vertices=6):
    radius_end = radius_start if radius_end is None else radius_end
    start, end = Vector(start), Vector(end)
    delta = end - start
    midpoint = (start + end) * 0.5
    obj = cone(name, midpoint, radius_start, radius_end, delta.length, vertices=vertices)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(delta.normalized())
    apply_transform(obj)
    return obj


def build_panther_surfaces():
    parts = []
    parts += [
        ico("torso", (0.2, 0, 2.86), (3.28, 0.78, 0.92), subdivisions=2),
        ico("shoulders", (-2.3, -0.02, 2.84), (1.22, 0.86, 1.16), rotation=(0, -0.2, 0), subdivisions=2),
        ico("haunches", (2.4, 0.02, 2.82), (1.24, 0.84, 1.1), rotation=(0, 0.12, 0), subdivisions=2),
        ico("neck", (-3.08, 0, 3.18), (0.98, 0.68, 0.96), rotation=(0, -0.42, 0), subdivisions=1),
        ico("head", (-4.02, -0.02, 3.5), (1.08, 0.65, 0.7), rotation=(0, 0.08, 0), subdivisions=2),
        ico("muzzle", (-4.88, -0.08, 3.18), (0.64, 0.5, 0.38), rotation=(0, -0.1, 0), subdivisions=1),
    ]

    # Ears and brow planes strengthen the feline silhouette.
    parts += [
        cone("ear_near", (-4.2, -0.42, 4.15), 0.34, 0.025, 0.65, rotation=(0.03, -0.2, 0.05), vertices=4),
        cone("ear_far", (-3.73, 0.38, 4.13), 0.31, 0.025, 0.6, rotation=(-0.04, -0.12, -0.08), vertices=4),
    ]

    # Four weight-bearing legs with different joint angles for a prowling stance.
    leg_specs = [
        ((-2.4, -0.54, 2.48), (-2.5, -0.58, 1.35), (-2.76, -0.6, 0.3), (-2.98, -0.64, 0.12)),
        ((-1.42, 0.48, 2.45), (-1.0, 0.5, 1.42), (-1.16, 0.52, 0.31), (-1.42, 0.54, 0.13)),
        ((2.12, -0.52, 2.42), (1.7, -0.56, 1.35), (2.22, -0.58, 0.35), (2.48, -0.61, 0.14)),
        ((2.82, 0.46, 2.4), (3.1, 0.48, 1.42), (3.0, 0.5, 0.32), (3.28, 0.52, 0.14)),
    ]
    for index, (hip, knee, ankle, paw) in enumerate(leg_specs):
        parts.append(cylinder_between(f"leg_{index}_upper", hip, knee, 0.34, 0.25))
        parts.append(cylinder_between(f"leg_{index}_lower", knee, ankle, 0.24, 0.16))
        parts.append(ico(f"paw_{index}", paw, (0.54, 0.36, 0.17), subdivisions=1))

    # Tail is a segmented taper, lifted at the tip.
    tail_points = [
        (3.15, 0.18, 3.15), (4.05, 0.2, 2.82), (4.78, 0.18, 2.25),
        (5.28, 0.14, 1.72), (5.72, 0.08, 1.52), (6.08, 0.0, 1.88),
    ]
    for index in range(len(tail_points) - 1):
        radius = 0.25 - index * 0.028
        parts.append(cylinder_between(f"tail_{index}", tail_points[index], tail_points[index + 1], radius, radius * 0.82, vertices=6))

    return parts


def shard_from_triangle(name, points, normal, gold, dark_gold, rng):
    centroid = sum(points, Vector()) / 3
    thickness = 0.026
    front = [point - centroid + normal * thickness for point in points]
    back = [point - centroid - normal * thickness for point in points]
    verts = front + back
    faces = [
        (0, 1, 2), (5, 4, 3),
        (0, 3, 4), (0, 4, 1),
        (1, 4, 5), (1, 5, 2),
        (2, 5, 3), (2, 3, 0),
    ]
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(gold)
    mesh.materials.append(dark_gold)
    for poly in mesh.polygons:
        poly.material_index = 0 if poly.index < 2 else 1
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = centroid

    final_location = centroid.copy()
    direction = Vector((centroid.x + 0.4, centroid.y * 1.8, centroid.z - 2.5))
    if direction.length < 0.01:
        direction = Vector((1, 0, 0))
    direction.normalize()
    distance = rng.uniform(1.55, 3.15)
    tangent = Vector((-direction.z, rng.uniform(-0.35, 0.35), direction.x))
    start_location = final_location + direction * distance + tangent * rng.uniform(-0.5, 0.5)
    start_rotation = (
        rng.uniform(-0.28, 0.28),
        rng.uniform(-0.34, 0.34),
        rng.uniform(-0.24, 0.24),
    )

    obj["start_position"] = list(start_location)
    obj["final_position"] = list(final_location)
    obj.location = start_location
    obj.rotation_euler = start_rotation
    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert("location", frame=1)
    obj.keyframe_insert("rotation_euler", frame=1)
    obj.keyframe_insert("scale", frame=1)

    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert("scale", frame=56)

    obj.location = final_location
    obj.rotation_euler = (0, 0, 0)
    obj.keyframe_insert("location", frame=62)
    obj.keyframe_insert("rotation_euler", frame=62)

    close_frame = rng.randint(84, 98)
    obj.scale = (1, 1, 1)
    obj.keyframe_insert("scale", frame=close_frame)
    obj.keyframe_insert("location", frame=120)
    obj.keyframe_insert("rotation_euler", frame=120)
    obj.keyframe_insert("scale", frame=120)

    return obj


def fracture(parts, gold, dark_gold):
    rng = random.Random(20260710)
    shards = []
    for part in parts:
        mesh = part.data
        for poly in mesh.polygons:
            if len(poly.vertices) != 3:
                continue
            points = [part.matrix_world @ mesh.vertices[index].co for index in poly.vertices]
            normal = (points[1] - points[0]).cross(points[2] - points[0]).normalized()
            shards.append(shard_from_triangle(f"shard_{len(shards):04d}", points, normal, gold, dark_gold, rng))
    for part in parts:
        bpy.data.objects.remove(part, do_unlink=True)
    return shards


def create_wire_network(shards, wire_material):
    starts = [Vector(obj["start_position"]) for obj in shards]
    finals = [Vector(obj["final_position"]) for obj in shards]
    edges = set()

    # Fixed nearest-neighbor topology: only vertex positions deform.
    for index, point in enumerate(finals):
        nearest = sorted(
            ((point - other).length_squared, other_index)
            for other_index, other in enumerate(finals)
            if other_index != index
        )[:3]
        for _, other_index in nearest:
            edges.add(tuple(sorted((index, other_index))))

    # Join any local nearest-neighbor clusters with the shortest available
    # bridges so the lattice is one connected component at every frame.
    parents = list(range(len(finals)))

    def find(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(a, b):
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            return False
        parents[root_b] = root_a
        return True

    for a, b in edges:
        union(a, b)
    component_count = len({find(index) for index in range(len(finals))})
    candidates = sorted(
        ((finals[a] - finals[b]).length_squared, a, b)
        for a in range(len(finals))
        for b in range(a + 1, len(finals))
    )
    for _, a, b in candidates:
        if union(a, b):
            edges.add((a, b))
            component_count -= 1
        if component_count == 1:
            break

    mesh = bpy.data.meshes.new("Connected Panther Lattice")
    mesh.from_pydata(starts, sorted(edges), [])
    network = bpy.data.objects.new("Connected Panther Lattice", mesh)
    bpy.context.collection.objects.link(network)

    network.shape_key_add(name="Dispersed")
    panther_key = network.shape_key_add(name="Panther")
    for index, point in enumerate(finals):
        panther_key.data[index].co = point
    panther_key.value = 0
    panther_key.keyframe_insert("value", frame=1)
    panther_key.keyframe_insert("value", frame=12)
    panther_key.value = 1
    panther_key.keyframe_insert("value", frame=62)
    panther_key.keyframe_insert("value", frame=120)

    group = bpy.data.node_groups.new("Connected Lattice Geometry", "GeometryNodeTree")
    group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nodes = group.nodes
    links = group.links
    group_in = nodes.new("NodeGroupInput")
    group_out = nodes.new("NodeGroupOutput")

    mesh_to_curve = nodes.new("GeometryNodeMeshToCurve")
    profile = nodes.new("GeometryNodeCurvePrimitiveCircle")
    profile.inputs["Resolution"].default_value = 3
    profile.inputs["Radius"].default_value = 0.022
    profile.inputs["Radius"].keyframe_insert("default_value", frame=1)
    profile.inputs["Radius"].keyframe_insert("default_value", frame=72)
    profile.inputs["Radius"].default_value = 0.0005
    profile.inputs["Radius"].keyframe_insert("default_value", frame=94)
    curve_to_mesh = nodes.new("GeometryNodeCurveToMesh")

    mesh_to_points = nodes.new("GeometryNodeMeshToPoints")
    mesh_to_points.mode = "VERTICES"
    node_sphere = nodes.new("GeometryNodeMeshIcoSphere")
    node_sphere.inputs["Radius"].default_value = 0.052
    node_sphere.inputs["Radius"].keyframe_insert("default_value", frame=1)
    node_sphere.inputs["Radius"].keyframe_insert("default_value", frame=72)
    node_sphere.inputs["Radius"].default_value = 0.0005
    node_sphere.inputs["Radius"].keyframe_insert("default_value", frame=94)
    node_sphere.inputs["Subdivisions"].default_value = 1
    instances = nodes.new("GeometryNodeInstanceOnPoints")
    join = nodes.new("GeometryNodeJoinGeometry")
    set_material = nodes.new("GeometryNodeSetMaterial")
    set_material.inputs["Material"].default_value = wire_material

    links.new(group_in.outputs["Geometry"], mesh_to_curve.inputs["Mesh"])
    links.new(mesh_to_curve.outputs["Curve"], curve_to_mesh.inputs["Curve"])
    links.new(profile.outputs["Curve"], curve_to_mesh.inputs["Profile Curve"])
    links.new(group_in.outputs["Geometry"], mesh_to_points.inputs["Mesh"])
    links.new(mesh_to_points.outputs["Points"], instances.inputs["Points"])
    links.new(node_sphere.outputs["Mesh"], instances.inputs["Instance"])
    links.new(curve_to_mesh.outputs["Mesh"], join.inputs["Geometry"])
    links.new(instances.outputs["Instances"], join.inputs["Geometry"])
    links.new(join.outputs["Geometry"], set_material.inputs["Geometry"])
    links.new(set_material.outputs["Geometry"], group_out.inputs["Geometry"])

    modifier = network.modifiers.new("Connected illuminated lattice", "NODES")
    modifier.node_group = group
    return network, len(edges)


def animate_detail(obj, material_slot, appear=82):
    obj.data.materials.append(material_slot)
    final_scale = obj.scale.copy()
    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert("scale", frame=1)
    obj.keyframe_insert("scale", frame=appear)
    obj.scale = final_scale
    obj.keyframe_insert("scale", frame=appear + 12)
    obj.keyframe_insert("scale", frame=120)


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup_scene():
    reset_scene()
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(FRAME_DIR, exist_ok=True)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1280 if ANIMATION else 960
    scene.render.resolution_y = 720 if ANIMATION else 540
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.fps = 30
    scene.frame_start = 1
    scene.frame_end = 120
    scene.world.use_nodes = True
    world_bg = scene.world.node_tree.nodes.get("Background")
    world_bg.inputs["Color"].default_value = (0.002, 0.004, 0.012, 1.0)
    world_bg.inputs["Strength"].default_value = 0.08

    gold = material("Brushed Gold", (0.72, 0.42, 0.08), metallic=0.88, roughness=0.23)
    dark_gold = material("Gold Edges", (0.18, 0.075, 0.012), metallic=0.72, roughness=0.34)
    wire_gold = material("Illuminated Lattice", (0.82, 0.42, 0.04), metallic=0.35, roughness=0.22, emission=(1.0, 0.34, 0.025))
    wire_gold.node_tree.nodes.get("Principled BSDF").inputs["Emission Strength"].default_value = 1.35
    eye_black = material("Obsidian Details", (0.006, 0.004, 0.003), metallic=0.25, roughness=0.18)
    eye_glow = material("Panther Eye", (0.85, 0.38, 0.02), metallic=0.1, roughness=0.15, emission=(1.0, 0.18, 0.01))
    floor_mat = material("Noir Floor", (0.006, 0.009, 0.018), metallic=0.12, roughness=0.28)

    parts = build_panther_surfaces()
    shards = fracture(parts, gold, dark_gold)
    network, edge_count = create_wire_network(shards, wire_gold)

    eye_socket = ico("Eye Socket", (-4.34, -0.62, 3.57), (0.2, 0.055, 0.12), subdivisions=1)
    animate_detail(eye_socket, eye_black)
    eye = ico("Illuminated Eye", (-4.39, -0.67, 3.58), (0.085, 0.026, 0.052), subdivisions=1)
    animate_detail(eye, eye_glow, appear=86)
    nose = ico("Obsidian Nose", (-5.38, -0.1, 3.06), (0.25, 0.42, 0.2), subdivisions=1)
    animate_detail(nose, eye_black, appear=84)

    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.08))
    floor = bpy.context.object
    floor.name = "Noir Floor"
    floor.data.materials.append(floor_mat)

    bpy.ops.object.light_add(type="AREA", location=(-4.5, -6.5, 9.0))
    key = bpy.context.object
    key.name = "Gold Key"
    key.data.energy = 1450
    key.data.shape = "DISK"
    key.data.size = 5.5
    key.data.color = (1.0, 0.68, 0.28)
    look_at(key, (-0.5, 0, 2.4))

    bpy.ops.object.light_add(type="AREA", location=(4.5, 2.8, 6.8))
    rim = bpy.context.object
    rim.name = "Cool Rim"
    rim.data.energy = 1050
    rim.data.size = 4.0
    rim.data.color = (0.18, 0.32, 0.62)
    look_at(rim, (1.0, 0, 2.6))

    bpy.ops.object.light_add(type="AREA", location=(0, -1.5, 10.0))
    top = bpy.context.object
    top.data.energy = 900
    top.data.size = 3.0
    top.data.color = (1.0, 0.86, 0.55)
    look_at(top, (0, 0, 2.0))

    bpy.ops.object.camera_add(location=(-0.3, -15.5, 5.1))
    camera = bpy.context.object
    camera.name = "Hero Camera"
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 12.7
    look_at(camera, (0.25, 0, 2.25))
    scene.camera = camera

    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.image_settings.color_mode = "RGBA"
    print(f"Connected {len(shards)} nodes with {edge_count} fixed edges")
    return scene, shards


scene, shards = setup_scene()
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VIDEO_DIR, "panther-shards.blend"))

if PREVIEW:
    scene.frame_set(18)
    scene.render.filepath = os.path.join(VIDEO_DIR, "panther-wire-preview.png")
    bpy.ops.render.render(write_still=True)
    scene.frame_set(62)
    scene.render.filepath = os.path.join(VIDEO_DIR, "panther-wireframe-preview.png")
    bpy.ops.render.render(write_still=True)
    scene.frame_set(110)
    scene.render.filepath = os.path.join(VIDEO_DIR, "panther-shards-preview.png")
    bpy.ops.render.render(write_still=True)
elif ANIMATION:
    scene.render.filepath = os.path.join(FRAME_DIR, "frame_")
    bpy.ops.render.render(animation=True)

print(f"Built {len(shards)} physical shards")
