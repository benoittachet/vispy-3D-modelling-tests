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

vispy.use('PyQt5')

#def update(ev):
#    global t, surface1, surface2, surface3, dimt    
#    
#    if (t % 2 == 1):
#        print("loop %d/%d" % (t, dimt))
#    #    if (hot_data[:, :, :, t].max() == 1):
#    #        surface1.parent = None
#        if (cool_data[:, :, :, t - 1].max() == 1):
#            surface2.parent = None
#    #    if (cold_data[:, :, :, t].max() == 1):
#    #        surface3.parent = None
#    #    if (hot_data[:, :, :, t].max() == 1):
#    #        surface1 = scene.visuals.Isosurface(hot_data[:, :, :, t], 1/1000,
#    #                                   color=(1, 0.6, 0.6, 1), shading='smooth',
#    #                                   parent=view.scene)
#    #        surface1.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
#    
#        if cool_data[:, :, :, t - 1].max() == 1:
#            verticesList = surface2.mesh_data.get_vertices();
#            verticesList = surface2.mesh_data.get_vertices();
#            facesList = surface2.mesh_data.get_faces()
#            print(cool_data[:, :, :, t].max())
#            print(verticesList)
#            print(facesList)
#                
#        if cool_data[:, :, :, t].max() == 1:
#            
#            surface2 = scene.visuals.Isosurface(cool_data[:, :, :, t], cool_data[:, :, :, t].max() / 4,
#                                       color=(0.8, 0.6, 0.8, 1), shading='smooth', 
#                                      parent=view.scene)
#    #        for i in range(0, np.shape(surface2.mesh_data.get_vertices())[0]):
#    #            surface2._vertex_colors= np.append(surface2._vertex_colors, [[0.8, 0.6, 0.8, 1]], axis=0)
#    #        nbVertex = np.shape(surface2.mesh_data.get_vertices())[0]
#    #        vertex_colors = np.zeros([nbVertex, 3])
#    #        for i in range(0, nbVertex):
#    #            vertex_colors[i] = np.array([0.8, 0.6, 0.8])
#    #        surface2._vertex_colors = vertex_colors
#            surface2.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
#            
#            
#            #edgesList = surface2.mesh_data.get_edges()
#    
#            #surface2.parent = None
#    #    if cold_data[:, :, :, t].max() == 1:
#    #        surface3 = scene.visuals.Isosurface(cold_data[:, :, :, t], 1/1000,
#    #                                   color=(0.6, 0.6, 1, 0.2), shading='smooth',
#    #                                   parent=view.scene)
#    #        surface3.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
#    
#        
#    t += 1
##   

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
    surface1.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
else:
    surface1 = scene.visuals.Isosurface(None, 1/1000,
                                       color=(1, 0.6, 0.6, 1), shading='smooth',
                                       parent=None)

if cool_data[:, :, :, 0].max() == 1:
    surface2 = scene.visuals.Isosurface(cool_data[:, :, :, 0], 0.1,
                               color=(1, 1, 0.6, 0.6), shading='smooth',
                               parent=view.scene)
    surface2.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
else:
    surface2 = scene.visuals.Isosurface(None, 1/1000,
                                       color=(1, 1, 0.6, 0.2), shading='smooth',
                                       parent=None)

no_data = [[[0]], [[0]], [[0]]]

if cold_data[:, :, :, 0].max() == 1:
    print("display cold data")
    surface3 = scene.visuals.Isosurface(cold_data[:, :, :, 0],
                               color=(0.6, 0.6, 1, 0.2), shading='smooth',
                               parent=view.scene)
    surface3.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
else:
    print("no display cold data")
    surface3 = scene.visuals.Isosurface(no_data, 1/1000,
                                       color=(1, 0.6, 0.6, 1), shading='smooth',
                                       parent=None)
    
coldMeshEdges = scene.visuals.Mesh(None, mode='lines', parent=view.scene)
coolMeshEdges = scene.visuals.Mesh(None, mode='lines', parent=view.scene)
hotMeshEdges = scene.visuals.Mesh(None, mode='lines', parent=view.scene)

# Add a 3D axis to keep us oriented
axis = scene.visuals.XYZAxis(parent=view.scene)

# Use a 3D camera
# Manual bounds; Mesh visual does not provide bounds yet
# Note how you can set bounds before assigning the camera to the viewbox
cam = scene.TurntableCamera(elevation=30, azimuth=30)
cam.set_range((-10, 10), (-10, 10), (-10, 10))
view.camera = cam

@canvas.events.mouse_press.connect
def on_mouse_press(event):
    global t, surface1, surface2
    print("loop %d/%d" % (t, dimt))
    
    if cold_data[:, :, :, t - 1].max() == 1 and t > 0:
        verticesList = surface3.mesh_data.get_vertices();
        facesList = surface3.mesh_data.get_faces()
        coldMeshEdges.set_data(verticesList, facesList, color=(0.6, 0.6, 1, 1))
        coldMeshEdges.parent = view.scene    
        coldMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing cold surface %d" % (t - 1))
    else:
        coldMeshEdges.parent = None
        
    if cold_data[:, :, :, t].max() == 1:
        
        print("display cold data")
        surface3.set_data(cold_data[:, :, :, t])
        surface3.parent = view.scene
        surface3.color=(1, 1, 0.6, 1)
        surface3.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
        
        
    if cool_data[:, :, :, t - 1].max() == 1 and t > 0:
        print("drawing cool structure")
        verticesList = surface2.mesh_data.get_vertices();
        facesList = surface2.mesh_data.get_faces()
        coolMeshEdges.set_data(verticesList, facesList, color=(1, 1, 0.6, 1))
        coolMeshEdges.parent = view.scene    
        coolMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing cool surface %d" % (t - 1))
    else:
        coolMeshEdges.parent = None
        
    if cool_data[:, :, :, t].max() == 1:
        
        print("display cool data")
        surface2.set_data(cool_data[:, :, :, t])
        surface2.parent = view.scene
        surface2.color=(1, 1, 0.6, 1)
        surface2.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
        
        
    if hot_data[:, :, :, t - 1].max() == 1 and t > 0:
        verticesList = surface1.mesh_data.get_vertices();
        facesList = surface1.mesh_data.get_faces()
        hotMeshEdges.set_data(verticesList, facesList, color=(1, 0.6, 0.6, 1))
        hotMeshEdges.parent = view.scene    
        hotMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing surface %d" % (t - 1))
    else:
        hotMeshEdges.parent = None
        
    if hot_data[:, :, :, t].max() == 1:
        
        print("display hot data")
        surface1.set_data(hot_data[:, :, :, t])
        surface1.parent = view.scene
        surface1.color=(1, 1, 0.6, 1)
        surface1.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
#        surface2.parent = None
        
    
    print("t = %i" % t)
    t += 1 


@canvas.events.key_press.connect
def on_key_press(event):
    global t, surface1, surface2
    print("loop %d/%d" % (t, dimt))
    
    if cold_data[:, :, :, t - 1].max() == 1 and t > 0:
        verticesList = surface3.mesh_data.get_vertices();
        facesList = surface3.mesh_data.get_faces()
        coldMeshEdges.set_data(verticesList, facesList, color=(0.6, 0.6, 1, 1))
        coldMeshEdges.parent = view.scene    
        coldMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing cold surface %d" % (t - 1))
        
    if cold_data[:, :, :, t].max() == 1:
        
        print("display cold data")
        surface3.set_data(cold_data[:, :, :, t])
        surface3.parent = view.scene
        surface3.color=(1, 1, 0.6, 1)
        surface3.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
        
        
    if cool_data[:, :, :, t - 1].max() == 1 and t > 0:
        print("drawing cool structure")
        verticesList = surface2.mesh_data.get_vertices();
        facesList = surface2.mesh_data.get_faces()
        coolMeshEdges.set_data(verticesList, facesList, color=(1, 1, 0.6, 1))
        coolMeshEdges.parent = view.scene    
        coolMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing cool surface %d" % (t - 1))
        
    if cool_data[:, :, :, t].max() == 1:
        
        print("display cool data")
        surface2.set_data(cool_data[:, :, :, t])
        surface2.parent = view.scene
        surface2.color=(1, 1, 0.6, 1)
        surface2.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
        
        
    if hot_data[:, :, :, t - 1].max() == 1 and t > 0:
        verticesList = surface1.mesh_data.get_vertices();
        facesList = surface1.mesh_data.get_faces()
        hotMeshEdges.set_data(verticesList, facesList, color=(1, 0.6, 0.6, 1))
        hotMeshEdges.parent = view.scene    
        hotMeshEdges.transform = scene.transforms.STTransform(translate=(-dimx / 2, -dimy / 2, -dimz / 2))
        print("drawing surface %d" % (t - 1))
        
    if hot_data[:, :, :, t].max() == 1:
        
        print("display hot data")
        surface1.set_data(hot_data[:, :, :, t])
        surface1.parent = view.scene
        surface1.color=(1, 1, 0.6, 1)
        surface1.transform = scene.transforms.STTransform(translate=(1000, 1000, 1000))
#        surface2.parent = None
        
    
    print("t = %i" % t)
    t += 1 

t =0

if __name__ == '__main__':
#    timer = app.Timer()
#    timer.connect(update)
#    timer.start(.1, 27)  # interval, iterations
    gloo.set_state(blend=True)
    canvas.show()
    if sys.flags.interactive == 0:
        app.run()