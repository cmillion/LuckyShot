# This is just a quick script for reading .ser movie files.
import numpy as np
import struct

def readheader(filename):
    header = {}
    with open(filename,'rb') as f:
        header['FileID'] = f.read(14) #str
        # Do an incredibly naive sanity check on the data
        if not header['FileID'] == 'LUCAM-RECORDER':
            print 'This is not a .ser formatted file.'
        header['LuID'] = struct.unpack('<I',f.read(4))[0] #int32
        header['ColorID'] = struct.unpack('<I',f.read(4))[0] #int32
        header['LittleEndian'] = struct.unpack('<I',f.read(4))[0] #int32
        header['ImageWidth'] = struct.unpack('<I',f.read(4))[0] #int32
        header['ImageHeight'] = struct.unpack('<I',f.read(4))[0] #int32
        header['PixelDepth'] = struct.unpack('<I',f.read(4))[0] #int32
        header['BytePerPixel'] = 1 if PixelDepth<=8 else 2
        header['FrameCount'] = struct.unpack('<I',f.read(4))[0] #int32
        header['Observer'] = struct.unpack('<40s',f.read(40))[0] #str
        header['Instrument'] = struct.unpack('<40s',f.read(40))[0] #str
        header['Telescope'] = struct.unpack('<40s',f.read(40))[0] #str
        header['DateTime'] = struct.unpack('<8s',f.read(8))[0] #"Date"
        header['DateTime_UTC'] = struct.unpack('<8s',f.read(8))[0] #"Date"

    return header

def readframe(filename,frame,header=False):
    if not header:
        header = readheader(filename)
    if frame > header['FrameCount']-1:
        print 'Frame #{frame} requested of {count} available.'.format(
                                                frame=frame, count=FrameCount)
        return False
    HeaderBytes = 178
    ImagePixels = header['ImageWidth']*header['ImageHeight']
    ImageBytes = ImagePixels*header['BytePerPixel']
    with open(filename,'rb') as f:
        f.seek(HeaderBytes+ImageBytes*WhichFrame)
        f.read(ImageBytes)
        fmt = '{endian}{pixels}{fmt}'.format(
                            endian='<' if header['LittleEndian'] else '>',
                            pixels=ImagePixels,
                            fmt='H' if BytePerPixel==2 else 'B')
        img = np.array(struct.unpack(fmt,f.read(ImageBytes))).reshape(ImageHeight,ImageWidth)

    return img, header

