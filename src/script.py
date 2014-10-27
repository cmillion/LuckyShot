%pylab
import ser
import scipy.ndimage
import MCUtils as mc

WesleyRelpath = '../../../Lucky/Wesley Uranus Storm Data New/20141002/'
WesleyFiles = ['20141002_131357_R650.ser','20141002_144929_R650.ser',
               '20141002_133006_R650.ser','20141002_151119_R650.ser',
               '20141002_134850_R650.ser','20141002_152709_R650.ser',
               '20141002_141500_R650.ser','20141002_154854_R650.ser',
               '20141002_143310_R650.ser','20141002_160535_R650.ser']
DelcroixRelpath = ('../../../Lucky/Delcroix Uranus Storm Data/'
                                        'uranus_20141003-04_ir685_PicDuMidi/')
DelcroixFiles = ['ir685_1/2014-10-03-2242_5-MD-IR685-8.ser',
                 'ir685_1/2014-10-03-2250_5-MD-IR685-9.ser',
                 'ir685_1/2014-10-03-2258_5-MD-IR685-10.ser',
                 'ir685_1/2014-10-03-2306_5-MD-IR685-11.ser',
                 'ir685_1/2014-10-03-2314_6-MD-IR685-12.ser',
                 'ir685_1/2014-10-03-2322_6-MD-IR685-13.ser',
                 'ir685_2/2014-10-03-2336_5-MD-IR685-15.ser',
                 'ir685_2/2014-10-03-2344_5-MD-IR685-16.ser',
                 'ir685_2/2014-10-03-2352_5-MD-IR685-17.ser',
                 'ir685_2/2014-10-04-0000_5-MD-IR685-18.ser',
                 'ir685_2/2014-10-04-0008_6-MD-IR685-19.ser',
                 'ir685_2/2014-10-04-0016_6-MD-IR685-20.ser',
                 'ir685_2/2014-10-04-0024_6-MD-IR685-21.ser',
                 'ir685_2/2014-10-04-0040_7-MD-IR685-23.ser',
                 'ir685_2/2014-10-04-0048_7-MD-IR685-24.ser',
                 'ir685_2/2014-10-04-0056_7-MD-IR685-25.ser',
                 'ir685_2/2014-10-04-0104_7-MD-IR685-26.ser',
                 'ir685_2/2014-10-04-0112_8-MD-IR685-27.ser',
                 'ir685_2/2014-10-04-0120_8-MD-IR685-28.ser',
                 'ir685_3/2014-10-04-0144_2-MD-IR685-30.ser',
                 'ir685_3/2014-10-04-0203_4-MD-IR685-32.ser',
                 'ir685_3/2014-10-04-0221_2-MD-IR685-34.ser',
                 'ir685_3/2014-10-04-0243_4-MD-IR685-36.ser']
DelcroixDarks = ['ir685_1/2014-10-03-2331_8-MD-DARK-3.ser',
                 'ir685_2/2014-10-04-0129_8-MD-DARK-4.ser']

def compute_cobs(filename):
    header = ser.readheader(filename)
    count = header['FrameCount']
    # Initialize some arrays for stat tracking...
    cob_x, cob_y = np.zeros(count), np.zeros(count)
    flatcoadd = np.zeros([150,150])
    for i in range(count-1):
        mc.print_inline(i)
        img,header = ser.readframe(filename,i,header=header)
        # Trim the edges
        img = img[165:315,245:395]
        flatcoadd+=img
        # Do a naive cut of the noise
        #ix = np.where(img<0.35*img.max())
        a = img
        #a[ix] = 0
        xcentroid = np.where(a.sum(axis=0))[0].mean()
        xcentroid = (a.sum(axis=0)*np.arange(150)).mean()/a.sum(axis=0).mean()
        ycentroid = np.where(a.sum(axis=1))[0].mean()
        ycentroid = (a.sum(axis=1)*np.arange(150)).mean()/a.sum(axis=1).mean()
        cob_x[i] = xcentroid
        cob_y[i] = ycentroid
    return cob_x, cob_y

#for f in WesleyFiles:
header = ser.readheader(WesleyRelpath+WesleyFiles[0])
x,y=compute_cobs(WesleyRelpath+WesleyFiles[0])

plt.figure()
plt.plot(x,y,'.')

d = mc.distance(x,y,x.mean(),y.mean())
# Slice out occasional [0,0] cobs
ix = np.where((x>1) & (y>1))
plt.figure()
plt.hist(d[ix]-d[ix].mean(),bins=100)
ix = np.where((x>1) & (y>1))

w,h = header['ImageWidth'],header['ImageHeight']
img = np.zeros([h,w])
for i in range(header['FrameCount']-1):
    mc.print_inline(i)
    img += ser.readframe(WesleyRelpath+WesleyFiles[0],i,header=header)

scl = 10
dims = [100,100]
luckcoadd = np.zeros(dims)
intpcoadd = np.zeros([scl*dims[0],scl*dims[1]])
for i in range(header['FrameCount']-1):
    if -0.75<d[i]-d[ix].mean()<0.75:
        mc.print_inline('Coadding {i}'.format(i=i))
        img,header = ser.readframe(WesleyRelpath+f,i,header=header)
        # Trim the edges
        img = img[w/2.-dims[0]/2.:w/2.+dims[0]/2.,
                  h/2.-dims[1]/2.:h/2.+dims[1]/2.]
        luckcoadd += img
        intpcoadd += scipy.ndimage.interpolation.shift(
                     scipy.ndimage.interpolation.zoom(img/scl**2,scl),
                     (scl*round(y.mean()-y[i]),
                     scl*round(x.mean()-x[i])))

plt.imshow(np.sqrt(intpcoadd)[100:225,75:200],cmap=cm.jet)
