"""
Module to manage and handle moviepy
video frames.

Each moviepy video is a sequence of
frames. Each frame can be normal or
can have a second related frame that
is a mask frame.

The normal frame is a 'np.uint8' and
has a (height, width, 3) shape. The
range of values is [0, 255] for each
color channel (R, G, B), where 0 
means no color and 255 full color.
For example, a frame of a 720p video
would have a (720, 1280, 3) shape.

The mask frame is a 'np.float32' or
'np.float64' and has a (height,
width) shape. The range of values is
[0.0, 1.0] for each value, where 0.0
means completely transparent and 1.0
means completely opaque. For example,
a frame of a 720p video would have 
(720, 1280) shape.

A mask frame can be attached to a 
normal frame but not viceversa. So,
a normal frame can (or cannot) have
a mask frame attached.
"""