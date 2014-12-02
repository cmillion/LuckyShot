%pylab
import ser
import scipy.ndimage
import MCUtils as mc

# shot at 6.6fps
filenames = {'Wesley':
        {'path':'../../../Lucky/Wesley Uranus Storm Data New/20141002/',
         'files':['20141002_131357_R650.ser','20141002_144929_R650.ser',
                  '20141002_133006_R650.ser','20141002_151119_R650.ser',
                  '20141002_134850_R650.ser','20141002_152709_R650.ser',
                  '20141002_141500_R650.ser','20141002_154854_R650.ser',
                  '20141002_143310_R650.ser','20141002_160535_R650.ser']},
        'Delcroix':
        {'path':('../../../Lucky/Delcroix Uranus Storm Data/'
                                    'uranus_20141003-04_ir685_PicDuMidi/'),
         'files':['ir685_1/2014-10-03-2242_5-MD-IR685-8.ser',
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
                  'ir685_3/2014-10-04-0243_4-MD-IR685-36.ser']}}
DelcroixDarks = ['ir685_1/2014-10-03-2331_8-MD-DARK-3.ser',
                 'ir685_2/2014-10-04-0129_8-MD-DARK-4.ser']

cob = {}
qtest = {}
img = {}
scl=int(1)
for j,fn in enumerate(filenames['Wesley']['files'][0:1]):
    f = filenames['Wesley']['path']+fn
    header = ser.readheader(f)
    cnt = header['FrameCount']-5500
    cob[j] = np.zeros([cnt-1,2])
    qtest[j]={}
    qtest[j]['x']=np.zeros([cnt-1,5])
    qtest[j]['y']=np.zeros([cnt-1,5])
    img[j]={'naive':np.zeros([100*scl,100*scl]),
            'lucky':np.zeros([100*scl,100*scl]),
            'inter':np.zeros([header['ImageHeight'],header['ImageWidth']])}
    for i in range(cnt-1):
        frame = ser.readframe(f,i,header=header)
        frame = scipy.ndimage.interpolation.zoom(frame,scl)/scl**2.
        blurred = scipy.ndimage.gaussian_filter(frame,sigma=5)
        xhist_b = blurred.sum(axis=0)
        yhist_b = blurred.sum(axis=1)
        xc = np.where(xhist_b==xhist_b.max())[0][0]
        yc = np.where(yhist_b==yhist_b.max())[0][0]
        cob[j][i]=[xc,yc]
        subframe = frame[cob[j][i][1]-50*scl:cob[j][i][1]+50*scl,
                         cob[j][i][0]-50*scl:cob[j][i][0]+50*scl]
        img[j]['naive']+=subframe/cnt
        for k,n in enumerate([10,20,30,40,50]):
            qtest[j]['x'][i][k]=xhist_b[cob[j][i][0]-n*scl:
                                                cob[j][i][0]+n*scl].sum()
            qtest[j]['y'][i][k]=xhist_b[cob[j][i][1]-n*scl:
                                                cob[j][i][1]+n*scl].sum()
        #xq = (float(xhist_b[cob[j][i][0]-5*scl:cob[j][i][0]+5*scl].sum()) /
        #            xhist_b[cob[j][i][0]-10*scl:cob[j][i][0]+10*scl].sum())
        #yq = (float(yhist_b[cob[j][i][1]-5*scl:cob[j][i][1]+5*scl].sum()) /
        #            yhist_b[cob[j][i][1]-10*scl:cob[j][i][1]+10*scl].sum())
        #qtest[j][i]=[xq,yq]
        mc.print_inline('{j} {i} {xc} {yc} {xq} {yq}'.format(
                            j=j,i=i,xc=cob[j][i][0],yc=cob[j][i][1],
                            xq=qtest[j]['x'][i][1]/qtest[j]['x'][i][3],
                            yq=qtest[j]['y'][i][1]/qtest[j]['y'][i][3]))
    xrat = qtest[j]['x'][:,1]/qtest[j]['x'][:,3]
    yrat = qtest[j]['y'][:,1]/qtest[j]['y'][:,3]
    xrng = xrat.max()-xrat.min()
    yrng = yrat.max()-yrat.min()
    p = 0.2/2.
    ix = np.where((xrat>=xrat.mean()-xrng*p) & (xrat<=xrat.mean()+xrng*p) &
                  (yrat>=yrat.mean()-yrng*p) & (yrat<=yrat.mean()+yrng*p))
    print 'Coadding {n} lucky frames of {cnt}.'.format(n=ix[0].shape[0],cnt=cnt)
    for i in ix[0]:
        mc.print_inline('Coadding: {i}'.format(i=i))
        frame = ser.readframe(f,i,header=header)
        frame = scipy.ndimage.interpolation.zoom(frame,scl)/scl**2.
        subframe = frame[cob[j][i][1]-50*scl:cob[j][i][1]+50*scl,
                         cob[j][i][0]-50*scl:cob[j][i][0]+50*scl]
        xc,yc=scipy.ndimage.measurements.center_of_mass(subframe)
        xc=cob[j][i][0]-50+xc
        yc=cob[j][i][1]-50+yc
        img[j]['lucky']+=subframe/cnt

cob = {}
qtest = {}
img = {}
scl=int(1)
for j,fn in enumerate(filenames['Wesley']['files'][0:1]):
    f = filenames['Wesley']['path']+fn
    print 'Reading: {f}'.format(f=f)
    header = ser.readheader(f)
    cnt = header['FrameCount']#-5500
    cob[j] = np.zeros([cnt-1,2])
    qtest[j]={}
    qtest[j]['x']=np.zeros([cnt-1,5])
    qtest[j]['y']=np.zeros([cnt-1,5])
    img[j]={'inter':np.zeros([header['ImageHeight'],header['ImageWidth']])}
    for i in range(cnt-1):
        #mc.print_inline('Shift + adding: {i}'.format(i=i))
        frame = ser.readframe(f,i,header=header)
        blurred = scipy.ndimage.gaussian_filter(frame,sigma=5)
        xhist_b = blurred.sum(axis=0)
        yhist_b = blurred.sum(axis=1)
        # Find the sort-of peak
        xc = np.where(xhist_b==xhist_b.max())[0][0]
        yc = np.where(yhist_b==yhist_b.max())[0][0]
        # Pull out the region around there
        xhist_r = xhist_b[xc-10:xc+10]
        yhist_r = yhist_b[yc-10:yc+10]
        # Fit a second order polynomial
        xfit = np.polyfit(np.arange(xc-10,xc+10),xhist_r,2)
        yfit = np.polyfit(np.arange(yc-10,yc+10),yhist_r,2)
        # Find the root of the first derivative (i.e. the peak)
        xpeak = np.poly1d(xfit).deriv().r
        ypeak = np.poly1d(yfit).deriv().r
        vec = [header['ImageHeight']/2.-ypeak,header['ImageWidth']/2.-xpeak]
        subframe = scipy.ndimage.interpolation.shift(frame,vec)
        mc.print_inline('Shift and adding {j},{i} by {vec}'.format(
                                                    j=j,i=i,vec=vec))
        img[j]['inter']+=subframe/cnt

fig = plt.figure(figsize=(16,16))
w,h=header['ImageWidth']/2.,header['ImageHeight']/2.
for i in img.keys():
    plt.subplot(3,3,i,xticks=[],yticks=[])
    plt.imshow(img[i]['inter'][h-25:h+25,w-25:w+25],cmap=cm.gray)

d = mc.distance(cob[0][:,1],cob[0][:,0],240,320)

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
