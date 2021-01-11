#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 15:25:28 2020

@author: benoit
"""

import numpy as np
from vispy import app, scene, gloo
import sys
import vispy
from vispy.geometry.isosurface import isosurface
from vispy.io import write_mesh

vispy.use('PyQt5')

def retrieveIsosurfaceData(surface1, dimx, dimy, dimz):
    
    vertices, faces = isosurface(surface1._data, surface1._level)
    edges = np.empty((0, 2), int)

   
        
        
    for face in faces:
            
        edges = np.append(edges, np.array([[face[0], face[1]]]), axis=0)
        edges = np.append(edges, np.array([[face[0], face[2]]]), axis=0)
        edges = np.append(edges, np.array([[face[1], face[2]]]), axis=0)
        
    #modifying vertices to get an image centered on (0, 0, 0)
        
    #first, we need to get max and min values on each dimension :
        
    
        
    for vertice in vertices:
        vertice[0] = vertice[0] - (dimx / 2)
        vertice[1] = vertice[1] - (dimy / 2)
        vertice[2] = vertice[2] - (dimz / 2)
        
    return vertices, edges, faces

def update(ev):
    global t, surface1, surface2
    print("loop %d/%d" % (t, dimt))
    
    #cold data
    surface3.set_data(cold_data[:, :, :, t])
    if (cold_data[:, :, :, t].max() == 1):
        coldVertices, coldEdges, coldFaces = retrieveIsosurfaceData(surface3, dimx, dimy, dimz)
        coldMeshEdges.set_data(coldVertices, coldEdges, color=(0.6, 0.6, 1, 1))
        coldMeshFaces.set_data(coldVertices, coldFaces)
        write_mesh("cold_%d.obj" % t, coldMeshFaces.mesh_data.get_vertices(), coldMeshFaces.mesh_data.get_faces(), coldMeshFaces.mesh_data.get_vertex_normals(), None, "hot data", "obj", True, True)
    else:
        coldMeshEdges.set_data(None, None)
        coldMeshFaces.set_data(None, None)
        
    
    #cool data
    surface2.set_data(cool_data[:, :, :, t])
    if (cool_data[:, :, :, t].max() == 1):
        coolVertices, coolEdges, coolFaces = retrieveIsosurfaceData(surface2, dimx, dimy, dimz)
        coolMeshEdges.set_data(coolVertices, coolEdges, color=(1, 1, 0.6, 1))
        coolMeshFaces.set_data(coolVertices, coolFaces)
        write_mesh("cool_%d.obj" % t, coolMeshFaces.mesh_data.get_vertices(), coolMeshFaces.mesh_data.get_faces(), coolMeshFaces.mesh_data.get_vertex_normals(), None, "hot data", "obj", True, True)
    else:
        coolMeshEdges.set_data(None, None)
        coolMeshFaces.set_data(None, None)
    
    #hot data
    surface1.set_data(hot_data[:, :, :, t])
    if (hot_data[:, :, :, t].max() == 1):
        hotVertices, hotEdges, hotFaces = retrieveIsosurfaceData(surface1, dimx, dimy, dimz)
        hotMeshEdges.set_data(hotVertices, hotEdges, color=(1, 0.6, 0.6, 1))
        hotMeshFaces.set_data(hotVertices, hotFaces)
        write_mesh("hot_%d.obj" % t, hotMeshFaces.mesh_data.get_vertices(), hotMeshFaces.mesh_data.get_faces(), hotMeshFaces.mesh_data.get_vertex_normals(), None, "hot data", "obj", True, True)
    else:
        hotMeshEdges.set_data(None, None)
        hotMeshFaces.set_data(None, None)
    print("t = %i" % t)
    t += 1

data = data = np.load("temperature_nparray.npy")
datanew = data[125 - 20: 125 + 20, 150 - 20 : 150+20, :, :]

dimx, dimy, dimz, dimt = datanew.shape

hot_data = np.zeros([dimx, dimy, dimz, dimt])
cool_data = np.zeros([dimx, dimy, dimz, dimt])
cold_data = np.zeros([dimx, dimy, dimz, dimt])



#cold_data = np.where(datanew > 5, 1, 0)
cold_data = np.where(datanew < 10, datanew, 0)
cold_data = np.where(datanew > 5, 1, 0)



#cool_data = np.where(datanew > 10, 1, 0)
cool_data = np.where(datanew < 15, datanew, 0)
cool_data = np.where(datanew > 10, 1, 0)


hot_data = np.where(datanew > 15, 1, 0)

# Create a canvas with a 3D viewport
canvas = scene.SceneCanvas(keys='interactive', bgcolor=(0, 0, 0))
view = canvas.central_widget.add_view()


## Define a scalar field from which we will generate an isosurface

print("Generating scalar field..")

#cold_data = cold_data[:, :, :, 50]

dimx, dimy, dimz, dimt = hot_data.shape

if (hot_data[:, :, :, 0].max() == 1):
    surface1 = scene.visuals.Isosurface(hot_data[:, :, :, 0], 0.1,
                               color=(1, 0.6, 0.6, 1), shading='smooth',
                               parent=view.scene)
    hotVertices, hotEdges, hotFaces = retrieveIsosurfaceData(surface1, dimx, dimy, dimz)
    
else:
    surface1 = scene.visuals.Isosurface(None, 1/1000,
                                       color=(1, 0.6, 0.6, 1), shading='smooth',
                                       parent=None)
    hotVertices, hotEdges, hotFaces = None, None, None

if cool_data[:, :, :, 0].max() == 1:
    surface2 = scene.visuals.Isosurface(cool_data[:, :, :, 0], 0.1,
                               color=(1, 1, 0.6, 0.6), shading='smooth',
                               parent=view.scene)
    coolVertices, coolEdges, coolFaces = retrieveIsosurfaceData(surface2, dimx, dimy, dimz)
    
else:
    surface2 = scene.visuals.Isosurface(None, 1/1000,
                                       color=(1, 1, 0.6, 1), shading='smooth',
                                       parent=None)
    coolVertices, coolEdges, coolFaces = None, None, None

no_data = [[[0]], [[0]], [[0]]]

if cold_data[:, :, :, 0].max() == 1:
    print("display cold data")
    surface3 = scene.visuals.Isosurface(cold_data[:, :, :, 0], 0.1,
                               color=(0.6, 0.6, 1, 1), shading='smooth',
                               parent=view.scene)
    coldVertices, coldEdges, coldFaces = retrieveIsosurfaceData(surface3, dimx, dimy, dimz)
    
else:
    print("no display cold data")
    surface3 = scene.visuals.Isosurface(no_data, 1/1000,
                                       color=(1, 0.6, 0.6, 1), shading='smooth',
                                       parent=None)
    coldVertices, coldEdges, coldFaces = None, None, None






if hotEdges != None and np.shape(hotEdges)[0] != 0:
    hotMeshEdges = scene.visuals.Mesh(hotVertices, hotEdges, mode='lines', parent=view.scene)
    hotMeshFaces = scene.visuals.Mesh(hotVertices, hotFaces, parent=None)
else:
    hotMeshEdges = scene.visuals.Mesh(None, None, mode='lines', parent=view.scene)
    hotMeshFaces = scene.visuals.Mesh(None, None, parent=None)
    
if coolEdges != None and np.shape(coolEdges)[0] != 0:
    coolMeshEdges = scene.visuals.Mesh(coolVertices, coolEdges, mode='lines', parent=view.scene)
    coolMeshFaces = scene.visuals.Mesh(coolVertices, coolFaces, parent=None)
else:
    coolMeshEdges = scene.visuals.Mesh(None, None, mode='lines', parent=view.scene)
    coolMeshFaces = scene.visuals.Mesh(None, None, parent=None)

if coldEdges != None and np.shape(coldEdges)[0] != 0:
    coldMeshEdges = scene.visuals.Mesh(coldVertices, coldEdges, mode='lines', parent=view.scene)
    coldMeshFaces = scene.visuals.Mesh(coldVertices, coldFaces, parent=None)
else:
    coldMeshEdges = scene.visuals.Mesh(None, None, mode='lines', parent=view.scene)
    coldMeshFaces = scene.visuals.Mesh(None, None, parent=None)

if hotMeshFaces.mesh_data.get_vertices() != None:
    write_mesh("hot_0.obj", hotMeshFaces.mesh_data.get_vertices(), hotMeshFaces.mesh_data.get_faces(), hotMeshFaces.mesh_data.get_vertex_normals(), None, "hot data", "obj", True, True)
if coolMeshFaces.mesh_data.get_vertices() != None:
    write_mesh("cool_0.obj", coolMeshFaces.mesh_data.get_vertices(), coolMeshFaces.mesh_data.get_faces(), coolMeshFaces.mesh_data.get_vertex_normals(), None, "cool data", "obj", True, True)
if coldMeshFaces.mesh_data.get_vertices() != None:
    write_mesh("cold_0.obj", coldMeshFaces.mesh_data.get_vertices(), coldMeshFaces.mesh_data.get_faces(), coldMeshFaces.mesh_data.get_vertex_normals(), None, "hot data", "obj", True, True)

# Add a 3D axis to keep us oriented
axis = scene.visuals.XYZAxis(parent=view.scene)

# Use a 3D camera
# Manual bounds; Mesh visual does not provide bounds yet
# Note how you can set bounds before assigning the camera to the viewbox
cam = scene.TurntableCamera(elevation=30, azimuth=30)
cam.set_range((-10, 10), (-10, 10), (-10, 10))
view.camera = cam

#@canvas.events.mouse_press.connect
#def on_mouse_press(event):
#@canvas.events.key_press.connect
#def on_key_press(event):
#    global t, surface1, surface2
#    print("loop %d/%d" % (t, dimt))
#    
#    #cold data
#    surface3.set_data(cold_data[:, :, :, t])
#    if (cold_data[:, :, :, t].max() == 1):
#        coldVertices, coldEdges = retrieveIsosurfaceData(surface3, dimx, dimy, dimz)
#        coldMeshEdges.set_data(coldVertices, coldEdges, color=(0.6, 0.6, 1, 1))
#    else:
#        coldMeshEdges.set_data(None, None)
#    
#    #cool data
#    surface2.set_data(cool_data[:, :, :, t])
#    if (cool_data[:, :, :, t].max() == 1):
#        coolVertices, coolEdges = retrieveIsosurfaceData(surface2, dimx, dimy, dimz)
#        coolMeshEdges.set_data(coolVertices, coolEdges, color=(1, 1, 0.6, 0.6))
#    else:
#        coolMeshEdges.set_data(None, None)
#    
#    #hot data
#    surface1.set_data(hot_data[:, :, :, t])
#    if (hot_data[:, :, :, t].max() == 1):
#        hotVertices, hotEdges = retrieveIsosurfaceData(surface1, dimx, dimy, dimz)
#        hotMeshEdges.set_data(hotVertices, hotEdges, color=(1, 0.6, 0.6, 1))
#    else:
#        hotMeshEdges.set_data(None, None)
#    print("t = %i" % t)
#    t += 1
#@canvas.events.key_press.connect
#def on_key_press(event):
#    global t, surface1, surface2
#    print("loop %d/%d" % (t, dimt))
#    
#    #cold data
#    surface3.set_data(cold_data[:, :, :, t])
#    coldVertices, coldEdges = retrieveIsosurfaceData(surface3)
#    coldMeshEdges.set_data(coldVertices, coldEdges, color=(0.6, .6, 1, 1))
#    
#    #cool data
#    surface2.set_data(cool_data[:, :, :, t])
#    coolVertices, coolEdges = retrieveIsosurfaceData(surface2)
#    coolMeshEdges.set_data(coolVertices, coolEdges, color=(1, 1, 0.6, 1))
#    
#    #hot data
#    surface1.set_data(hot_data[:, :, :, t])
#    hotVertices, hotEdges = retrieveIsosurfaceData(surface1)
#    hotMeshEdges.set_data(hotVertices, hotEdges, color=(1, 0.6, 0.6, 1))
#    
##    if cold_data[:, :, :, t - 1].max() == 1 and t > 0:
##        verticesList = surface3.mesh_data.get_vertices();
##        facesList = surface3.mesh_data.get_faces()
##        coldMeshEdges.set_data(verticesList, facesList, color=(0.6, 0.6, 1, 1))
##        coldMeshEdges.parent = view.scene    
##        coldMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
##        print("drawing cold surface %d" % (t - 1))
##        
##    if cold_data[:, :, :, t].max() == 1:
##        
##        print("display cold data")
##        surface3.set_data(cold_data[:, :, :, t])
##        surface3.parent = view.scene
##        surface3.color=(1, 1, 0.6, 1)
##        surface3.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
#        
#        
##    if cool_data[:, :, :, t - 1].max() == 1 and t > 0:
##        print("drawing cool structure")
##        verticesList = surface2.mesh_data.get_vertices();
##        facesList = surface2.mesh_data.get_faces()
##        coolMeshEdges.set_data(verticesList, facesList, color=(1, 1, 0.6, 1))
##        coolMeshEdges.parent = view.scene    
##        coolMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
##        print("drawing cool surface %d" % (t - 1))
##        
##    if cool_data[:, :, :, t].max() == 1:
##        
##        print("display cool data")
##        surface2.set_data(cool_data[:, :, :, t])
##        surface2.parent = view.scene
##        surface2.color=(1, 1, 0.6, 1)
##        surface2.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
#        
#        
##    if hot_data[:, :, :, t - 1].max() == 1 and t > 0:
##        verticesList = surface1.mesh_data.get_vertices();
##        facesList = surface1.mesh_data.get_faces()
##        hotMeshEdges.set_data(verticesList, facesList, color=(1, 0.6, 0.6, 1))
##        hotMeshEdges.parent = view.scene    
##        hotMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
##        print("drawing surface %d" % (t - 1))
##        
##    if hot_data[:, :, :, t].max() == 1:
##        
##        print("display hot data")
##        surface1.set_data(hot_data[:, :, :, t])
##        surface1.parent = view.scene
##        surface1.color=(1, 1, 0.6, 1)
##        surface1.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
###        surface2.parent = None
#        
#    
#    print("t = %i" % t)
#    t += 1 

t =0

if __name__ == '__main__':
    timer = app.Timer()
    timer.connect(update)
    timer.start(.1, dimt)  # interval, iterations
    gloo.set_state(blend=True)
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()