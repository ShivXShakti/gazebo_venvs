
shape_msgs::msg::Mesh mesh;
shapes::ShapeMsg mesh_msg;
shapes::Mesh* mesh_shape = shapes::createMeshFromResource("package://my_pkg/meshes/bottle.dae");
shapes::constructMsgFromShape(mesh_shape, mesh_msg);

moveit_msgs::msg::CollisionObject obj;
obj.id = "bottle";
obj.header.frame_id = "base_link";
obj.meshes.push_back(boost::get<shape_msgs::msg::Mesh>(mesh_msg));
obj.mesh_poses.push_back(pose);
obj.operation = obj.ADD;

planning_scene_interface.applyCollisionObject(obj);
