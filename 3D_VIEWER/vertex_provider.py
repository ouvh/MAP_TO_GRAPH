import math
import numpy
import random,time


def get_sphere_vertex(center:tuple,radius:float,layer_precision:float,curve_precision:float) -> list[tuple]:
    #x  = (math.sqrt(radius**2 - (start + i*((end-start)/layer_precision) - center[2])**2)) * math.cos(j*((2*math.pi)/curve_precision) + (((2*math.pi)/curve_precision)/2 if i%2==0 else 0))

    limit_error = 0
    start = center[2] - radius + limit_error
    end = center[2] + radius - limit_error
    layer = [ [ (center[0] + (math.sqrt(radius**2 - (start + i*((end-start)/layer_precision) - center[2])**2)) * math.cos(j*((2*math.pi)/curve_precision) + ( i*((math.pi)/curve_precision) )),center[1] + (math.sqrt(radius**2 - (start + i*((end-start)/layer_precision) - center[2])**2)) * math.sin(j*((2*math.pi)/curve_precision) + ( i*((math.pi)/curve_precision) )),start + i*((end-start)/layer_precision) ) for j in range(curve_precision)] for i in range(layer_precision + 1)]
    triangles = []

    for i in range(layer_precision):
        for j in range(curve_precision):
            triangles.append((layer[i][j],layer[i+1][j],layer[i][(j+1)%curve_precision]))
        
        for j in range(curve_precision):
            triangles.append((layer[i+1][j],layer[i][j],layer[i+1][(j+1)%curve_precision])[::-1])
       
    
    vertex = sum(triangles,start=tuple())
    normals = [(1,1,1) for _ in range(len(vertex))]

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])
    return vertex_data


def get_tunnel(center1:tuple,center2:tuple,thickness:float) -> list[tuple]:
    angle = (2*math.pi)/3
    normal = (center2[0] - center1[0],center2[1] - center1[1],center2[2] - center1[2])
    e = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    normal_1 = (normal[0]/e,normal[1]/e,normal[2]/e)

    d = -(normal[0]*center1[0] + normal[1]*center1[1] + normal[2]*center1[2])




    if normal[2] == 0:
        if normal[1] == 0:
            vecteur_directeur = (-d/normal[0],1,1)
            if vecteur_directeur == center1:
                vecteur_directeur = (-d/normal[0],1,2)

        else:
            vecteur_directeur = (1,-(d+normal[0])/normal[1],0)

            if vecteur_directeur == center1:
                vecteur_directeur = (2,-(d+2*normal[0])/normal[1],0)
    else:
        vecteur_directeur = (1,1,((-normal[0] - normal[1] - d)/normal[2]))

        if vecteur_directeur == center1:
            vecteur_directeur = (1,2,((-normal[0] - 2*normal[1] - d)/normal[2]))















    vecteur_directeur = (vecteur_directeur[0] - center1[0],vecteur_directeur[1] - center1[1],vecteur_directeur[2] - center1[2])

    norme = math.sqrt(vecteur_directeur[0]**2 + vecteur_directeur[1]**2 + vecteur_directeur[2]**2)
    vecteur_directeur = ((vecteur_directeur[0]/norme)*thickness,(vecteur_directeur[1]/norme)*thickness,(vecteur_directeur[2]/norme)*thickness)

    matrice = [
        [normal_1[0]**2 + (1 - normal_1[0]**2) * math.cos(angle), normal_1[0]*normal_1[1]*(1 - math.cos(angle)) - normal_1[2]*math.sin(angle), normal_1[0]*normal_1[2]*(1 - math.cos(angle)) + normal_1[1]*math.sin(angle)],
        [normal_1[0]*normal_1[1]*(1 - math.cos(angle)) + normal_1[2]*math.sin(angle), normal_1[1]**2 + (1 - normal_1[1]**2) * math.cos(angle), normal_1[1]*normal_1[2]*(1 - math.cos(angle)) - normal_1[0]*math.sin(angle)],
        [normal_1[0]*normal_1[2]*(1 - math.cos(angle)) - normal_1[1]*math.sin(angle), normal_1[1]*normal_1[2]*(1 - math.cos(angle)) + normal_1[0]*math.sin(angle), normal_1[2]**2 + (1 - normal_1[2]**2) * math.cos(angle)]
    ]

    vector1 = vecteur_directeur
    vector2 = produit_matrice(matrice,vector1)
    vector3 = produit_matrice(matrice,vector2)

    point_1 = somme_de_vecteur(center1, vector1)
    dual_point_1 = somme_de_vecteur(center2, vector1)

    point_2 = somme_de_vecteur(center1, vector2)
    dual_point_2 = somme_de_vecteur(center2, vector2)

    point_3 = somme_de_vecteur(center1, vector3)
    dual_point_3 = somme_de_vecteur(center2, vector3)


    triangles = [(point_2,dual_point_1,point_1),(point_2,dual_point_2,dual_point_1),(point_3,dual_point_1,dual_point_3),(point_1,dual_point_1,point_3),(point_2,dual_point_3,point_3),(point_2,dual_point_2,dual_point_3)]

    vertex = sum(triangles,start=tuple())
    normals = [(1,1,1) for _ in range(len(vertex))]

    vertex = numpy.array(vertex, dtype='f4')
    normals = numpy.array(normals, dtype='f4')
    vertex_data = numpy.hstack([normals, vertex])

    return vertex_data


def produit_matrice(matrice,vect):
    return (matrice[0][0]*vect[0] + matrice[0][1]*vect[1] + matrice[0][2]*vect[2],matrice[1][0]*vect[0] + matrice[1][1]*vect[1] + matrice[1][2]*vect[2],matrice[2][0]*vect[0] + matrice[2][1]*vect[1] + matrice[2][2]*vect[2])


def somme_de_vecteur(ver1,ver2):
    return (ver1[0] + ver2[0],ver1[1] + ver2[1],ver1[2] + ver2[2])