import os
import subprocess
import time
import importlib.metadata
import Oasys.gRPC


_connection = None
_debug      = False


def start(abspath, args=None, port=50051, memory=25, license=None, debug=False, batch=False, wait=5):
    if debug:
        print("Starting {}, listening on port {}".format(abspath, port))

    environ = os.environ.copy()
    if license:
        environ[ARUP_LICENSE_PATH] = license

    try:
        portnum = int(port)
        if portnum < 1:
            raise ValueError("Negative port number {} for PRIMER. Cannot continue".format(portnum))
    except:
        raise ValueError("Invalid port number {} for PRIMER. Cannot continue".format(port))

    pargs = [abspath, "-grpc=-{}".format(portnum)]
    if args:
        pargs.extend(args)
    if batch:
        pargs.append("-batch")

    proc = subprocess.Popen(pargs, env=environ)

# Sleep to give time for PRIMER to start
    time.sleep(wait)

    proc.poll()
    if proc.returncode == 99:
        raise ValueError("Failed to start PRIMER. Port {} already in use. Cannot continue".format(portnum))
    elif proc.returncode == 98:
        raise ValueError("Failed to start gRPC server in PRIMER. Cannot continue")
    elif proc.returncode:
        raise ValueError("Failed to start PRIMER. Cannot continue")

    return connect(portnum, memory, 'localhost', debug)


def connect(port=50051, memory=25, hostname='localhost', debug=False):
    if debug:
        print("Called connect with port {} and memory {}".format(port, memory))

    Oasys.PRIMER._debug      = debug
    Oasys.PRIMER._connection = Oasys.gRPC.Connection("PRIMER", port, memory, hostname, debug)

# Check version
    version  = importlib.metadata.version('Oasys.PRIMER')
    modMajor = int(version.split('.')[0]);
    exeMajor = int(Oasys.PRIMER._connection.version);

    if debug:
        print("Oasys.PRIMER module version {} ({})".format(modMajor, version))
        print("PRIMER executable version {} ({})".format(exeMajor, Oasys.PRIMER._connection.version))

    if exeMajor != modMajor:
        raise ValueError("Major version ({}) of PRIMER executable {} != major version ({}) of Oasys.PRIMER module {}. Cannot continue".format(exeMajor, Oasys.PRIMER._connection.version, modMajor, version))

    return Oasys.PRIMER._connection


def disconnect(connection):
    if Oasys.PRIMER._debug:
        print("Called disconnect")

    connection.finalise()
    Oasys.PRIMER._connection = None


def terminate(connection):
    if Oasys.PRIMER._debug:
        print("Called terminate")

    connection.terminate()
    Oasys.PRIMER._connection = None


def createInstance(t, h):
# Classes in PRIMER
    if t == "Accelerometer":
        instance = object.__new__(Oasys.PRIMER.Accelerometer)
    elif t == "Airbag":
        instance = object.__new__(Oasys.PRIMER.Airbag)
    elif t == "Attached":
        instance = object.__new__(Oasys.PRIMER.Attached)
    elif t == "AxialForceBeam":
        instance = object.__new__(Oasys.PRIMER.AxialForceBeam)
    elif t == "Beam":
        instance = object.__new__(Oasys.PRIMER.Beam)
    elif t == "Belt":
        instance = object.__new__(Oasys.PRIMER.Belt)
    elif t == "Box":
        instance = object.__new__(Oasys.PRIMER.Box)
    elif t == "Colour":
        instance = object.__new__(Oasys.PRIMER.Colour)
    elif t == "Comment":
        instance = object.__new__(Oasys.PRIMER.Comment)
    elif t == "ConnectionProperties":
        instance = object.__new__(Oasys.PRIMER.ConnectionProperties)
    elif t == "ConstructionStages":
        instance = object.__new__(Oasys.PRIMER.ConstructionStages)
    elif t == "Contact":
        instance = object.__new__(Oasys.PRIMER.Contact)
    elif t == "ContactGuidedCable":
        instance = object.__new__(Oasys.PRIMER.ContactGuidedCable)
    elif t == "Conx":
        instance = object.__new__(Oasys.PRIMER.Conx)
    elif t == "CoordinateSystem":
        instance = object.__new__(Oasys.PRIMER.CoordinateSystem)
    elif t == "CrossSection":
        instance = object.__new__(Oasys.PRIMER.CrossSection)
    elif t == "Curve":
        instance = object.__new__(Oasys.PRIMER.Curve)
    elif t == "DampingFrequencyRange":
        instance = object.__new__(Oasys.PRIMER.DampingFrequencyRange)
    elif t == "DampingPartMass":
        instance = object.__new__(Oasys.PRIMER.DampingPartMass)
    elif t == "DampingPartStiffness":
        instance = object.__new__(Oasys.PRIMER.DampingPartStiffness)
    elif t == "DampingPartStructural":
        instance = object.__new__(Oasys.PRIMER.DampingPartStructural)
    elif t == "DampingRelative":
        instance = object.__new__(Oasys.PRIMER.DampingRelative)
    elif t == "DeformableToRigid":
        instance = object.__new__(Oasys.PRIMER.DeformableToRigid)
    elif t == "Discrete":
        instance = object.__new__(Oasys.PRIMER.Discrete)
    elif t == "DiscreteSphere":
        instance = object.__new__(Oasys.PRIMER.DiscreteSphere)
    elif t == "Dummy":
        instance = object.__new__(Oasys.PRIMER.Dummy)
    elif t == "ElementDeath":
        instance = object.__new__(Oasys.PRIMER.ElementDeath)
    elif t == "ExtraNodes":
        instance = object.__new__(Oasys.PRIMER.ExtraNodes)
    elif t == "FreqFRF":
        instance = object.__new__(Oasys.PRIMER.FreqFRF)
    elif t == "FreqSSD":
        instance = object.__new__(Oasys.PRIMER.FreqSSD)
    elif t == "FreqVibration":
        instance = object.__new__(Oasys.PRIMER.FreqVibration)
    elif t == "GeneralizedWeld":
        instance = object.__new__(Oasys.PRIMER.GeneralizedWeld)
    elif t == "GeometrySurface":
        instance = object.__new__(Oasys.PRIMER.GeometrySurface)
    elif t == "Group":
        instance = object.__new__(Oasys.PRIMER.Group)
    elif t == "HexSpotweldAssembly":
        instance = object.__new__(Oasys.PRIMER.HexSpotweldAssembly)
    elif t == "History":
        instance = object.__new__(Oasys.PRIMER.History)
    elif t == "Hourglass":
        instance = object.__new__(Oasys.PRIMER.Hourglass)
    elif t == "IGA1DBrep":
        instance = object.__new__(Oasys.PRIMER.IGA1DBrep)
    elif t == "IGA1DNurbsUVW":
        instance = object.__new__(Oasys.PRIMER.IGA1DNurbsUVW)
    elif t == "IGA1DNurbsXYZ":
        instance = object.__new__(Oasys.PRIMER.IGA1DNurbsXYZ)
    elif t == "IGA2DBasisTransformXYZ":
        instance = object.__new__(Oasys.PRIMER.IGA2DBasisTransformXYZ)
    elif t == "IGA2DBrep":
        instance = object.__new__(Oasys.PRIMER.IGA2DBrep)
    elif t == "IGA2DNurbsUVW":
        instance = object.__new__(Oasys.PRIMER.IGA2DNurbsUVW)
    elif t == "IGA2DNurbsXYZ":
        instance = object.__new__(Oasys.PRIMER.IGA2DNurbsXYZ)
    elif t == "IGA3DBasisTransformXYZ":
        instance = object.__new__(Oasys.PRIMER.IGA3DBasisTransformXYZ)
    elif t == "IGA3DNurbsXYZ":
        instance = object.__new__(Oasys.PRIMER.IGA3DNurbsXYZ)
    elif t == "IGAEdgeUVW":
        instance = object.__new__(Oasys.PRIMER.IGAEdgeUVW)
    elif t == "IGAEdgeXYZ":
        instance = object.__new__(Oasys.PRIMER.IGAEdgeXYZ)
    elif t == "IGAFaceUVW":
        instance = object.__new__(Oasys.PRIMER.IGAFaceUVW)
    elif t == "IGAFaceXYZ":
        instance = object.__new__(Oasys.PRIMER.IGAFaceXYZ)
    elif t == "IGAIntegrationShellReduce":
        instance = object.__new__(Oasys.PRIMER.IGAIntegrationShellReduce)
    elif t == "IGAIntegrationSolidReduce":
        instance = object.__new__(Oasys.PRIMER.IGAIntegrationSolidReduce)
    elif t == "IGAMass":
        instance = object.__new__(Oasys.PRIMER.IGAMass)
    elif t == "IGAPointUVW":
        instance = object.__new__(Oasys.PRIMER.IGAPointUVW)
    elif t == "IGAShell":
        instance = object.__new__(Oasys.PRIMER.IGAShell)
    elif t == "IGASolid":
        instance = object.__new__(Oasys.PRIMER.IGASolid)
    elif t == "IGAVolumeXYZ":
        instance = object.__new__(Oasys.PRIMER.IGAVolumeXYZ)
    elif t == "Image":
        instance = object.__new__(Oasys.PRIMER.Image)
    elif t == "Include":
        instance = object.__new__(Oasys.PRIMER.Include)
    elif t == "IntegrationBeam":
        instance = object.__new__(Oasys.PRIMER.IntegrationBeam)
    elif t == "IntegrationShell":
        instance = object.__new__(Oasys.PRIMER.IntegrationShell)
    elif t == "InterfaceComponent":
        instance = object.__new__(Oasys.PRIMER.InterfaceComponent)
    elif t == "InterfaceLinkingEdge":
        instance = object.__new__(Oasys.PRIMER.InterfaceLinkingEdge)
    elif t == "InterfaceSpringback":
        instance = object.__new__(Oasys.PRIMER.InterfaceSpringback)
    elif t == "Interpolation":
        instance = object.__new__(Oasys.PRIMER.Interpolation)
    elif t == "InterpolationSpotweld":
        instance = object.__new__(Oasys.PRIMER.InterpolationSpotweld)
    elif t == "Joint":
        instance = object.__new__(Oasys.PRIMER.Joint)
    elif t == "JointStiffness":
        instance = object.__new__(Oasys.PRIMER.JointStiffness)
    elif t == "Linear":
        instance = object.__new__(Oasys.PRIMER.Linear)
    elif t == "LoadBeam":
        instance = object.__new__(Oasys.PRIMER.LoadBeam)
    elif t == "LoadBodyGeneralized":
        instance = object.__new__(Oasys.PRIMER.LoadBodyGeneralized)
    elif t == "LoadGravity":
        instance = object.__new__(Oasys.PRIMER.LoadGravity)
    elif t == "LoadNode":
        instance = object.__new__(Oasys.PRIMER.LoadNode)
    elif t == "LoadRemovePart":
        instance = object.__new__(Oasys.PRIMER.LoadRemovePart)
    elif t == "LoadRigidBody":
        instance = object.__new__(Oasys.PRIMER.LoadRigidBody)
    elif t == "LoadShell":
        instance = object.__new__(Oasys.PRIMER.LoadShell)
    elif t == "Mass":
        instance = object.__new__(Oasys.PRIMER.Mass)
    elif t == "MassPart":
        instance = object.__new__(Oasys.PRIMER.MassPart)
    elif t == "Material":
        instance = object.__new__(Oasys.PRIMER.Material)
    elif t == "Mechanism":
        instance = object.__new__(Oasys.PRIMER.Mechanism)
    elif t == "Model":
        instance = object.__new__(Oasys.PRIMER.Model)
    elif t == "MorphBox":
        instance = object.__new__(Oasys.PRIMER.MorphBox)
    elif t == "MorphFlow":
        instance = object.__new__(Oasys.PRIMER.MorphFlow)
    elif t == "MorphPoint":
        instance = object.__new__(Oasys.PRIMER.MorphPoint)
    elif t == "NodalForceGroup":
        instance = object.__new__(Oasys.PRIMER.NodalForceGroup)
    elif t == "NodalRigidBody":
        instance = object.__new__(Oasys.PRIMER.NodalRigidBody)
    elif t == "Node":
        instance = object.__new__(Oasys.PRIMER.Node)
    elif t == "NodeSet":
        instance = object.__new__(Oasys.PRIMER.NodeSet)
    elif t == "Options":
        instance = object.__new__(Oasys.PRIMER.Options)
    elif t == "Parameter":
        instance = object.__new__(Oasys.PRIMER.Parameter)
    elif t == "Part":
        instance = object.__new__(Oasys.PRIMER.Part)
    elif t == "PrescribedAccelerometerRigid":
        instance = object.__new__(Oasys.PRIMER.PrescribedAccelerometerRigid)
    elif t == "PrescribedFinalGeometry":
        instance = object.__new__(Oasys.PRIMER.PrescribedFinalGeometry)
    elif t == "PrescribedMotion":
        instance = object.__new__(Oasys.PRIMER.PrescribedMotion)
    elif t == "PrescribedOrientationRigid":
        instance = object.__new__(Oasys.PRIMER.PrescribedOrientationRigid)
    elif t == "Pretensioner":
        instance = object.__new__(Oasys.PRIMER.Pretensioner)
    elif t == "ReferenceGeometry":
        instance = object.__new__(Oasys.PRIMER.ReferenceGeometry)
    elif t == "Retractor":
        instance = object.__new__(Oasys.PRIMER.Retractor)
    elif t == "RigidBodies":
        instance = object.__new__(Oasys.PRIMER.RigidBodies)
    elif t == "Rigidwall":
        instance = object.__new__(Oasys.PRIMER.Rigidwall)
    elif t == "Seatbelt1D":
        instance = object.__new__(Oasys.PRIMER.Seatbelt1D)
    elif t == "Seatbelt2D":
        instance = object.__new__(Oasys.PRIMER.Seatbelt2D)
    elif t == "Section":
        instance = object.__new__(Oasys.PRIMER.Section)
    elif t == "Sensor":
        instance = object.__new__(Oasys.PRIMER.Sensor)
    elif t == "SensorControl":
        instance = object.__new__(Oasys.PRIMER.SensorControl)
    elif t == "SensorDefine":
        instance = object.__new__(Oasys.PRIMER.SensorDefine)
    elif t == "SensorSwitch":
        instance = object.__new__(Oasys.PRIMER.SensorSwitch)
    elif t == "SetK":
        instance = object.__new__(Oasys.PRIMER.Set)
    elif t == "Shell":
        instance = object.__new__(Oasys.PRIMER.Shell)
    elif t == "ShellReferenceGeometry":
        instance = object.__new__(Oasys.PRIMER.ShellReferenceGeometry)
    elif t == "Slipring":
        instance = object.__new__(Oasys.PRIMER.Slipring)
    elif t == "Solid":
        instance = object.__new__(Oasys.PRIMER.Solid)
    elif t == "Spc":
        instance = object.__new__(Oasys.PRIMER.Spc)
    elif t == "Sph":
        instance = object.__new__(Oasys.PRIMER.Sph)
    elif t == "Spotweld":
        instance = object.__new__(Oasys.PRIMER.Spotweld)
    elif t == "Spr2":
        instance = object.__new__(Oasys.PRIMER.Spr2)
    elif t == "StagedConstructionPart":
        instance = object.__new__(Oasys.PRIMER.StagedConstructionPart)
    elif t == "StrainBeam":
        instance = object.__new__(Oasys.PRIMER.StrainBeam)
    elif t == "StrainShell":
        instance = object.__new__(Oasys.PRIMER.StrainShell)
    elif t == "StrainSolid":
        instance = object.__new__(Oasys.PRIMER.StrainSolid)
    elif t == "StressBeam":
        instance = object.__new__(Oasys.PRIMER.StressBeam)
    elif t == "StressSection":
        instance = object.__new__(Oasys.PRIMER.StressSection)
    elif t == "StressShell":
        instance = object.__new__(Oasys.PRIMER.StressShell)
    elif t == "StressSolid":
        instance = object.__new__(Oasys.PRIMER.StressSolid)
    elif t == "Termination":
        instance = object.__new__(Oasys.PRIMER.Termination)
    elif t == "TieBreak":
        instance = object.__new__(Oasys.PRIMER.TieBreak)
    elif t == "Transformation":
        instance = object.__new__(Oasys.PRIMER.Transformation)
    elif t == "Tshell":
        instance = object.__new__(Oasys.PRIMER.Tshell)
    elif t == "Utils":
        instance = object.__new__(Oasys.PRIMER.Utils)
    elif t == "Vector":
        instance = object.__new__(Oasys.PRIMER.Vector)
    elif t == "Velocity":
        instance = object.__new__(Oasys.PRIMER.Velocity)
    elif t == "VelocityGeneration":
        instance = object.__new__(Oasys.PRIMER.VelocityGeneration)
    elif t == "View":
        instance = object.__new__(Oasys.PRIMER.View)
    elif t == "Window":
        instance = object.__new__(Oasys.PRIMER.Window)
    elif t == "Workflow":
        instance = object.__new__(Oasys.PRIMER.Workflow)
    elif t == "Xrefs":
        instance = object.__new__(Oasys.PRIMER.Xrefs)

# Generic object
    elif t == "ItemObject":
        instance = object.__new__(Oasys.PRIMER.ItemObject)

# Unsupported
    else:
        raise NotImplementedError("Instance type '{}' not implemented".format(t))

    instance.__dict__['_handle']  = h;
    instance.__dict__['_objtype'] = t;

    return instance
