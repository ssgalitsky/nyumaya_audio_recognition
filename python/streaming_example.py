import time
import os
import argparse
import sys
import datetime

sys.path.append('./src')

from libnyumaya import AudioRecognition,FeatureExtractor
from auto_platform import AudiostreamSource, play_command,default_libpath



def label_stream(labels,libpath ,graph,sensitivity):

	audio_stream = AudiostreamSource()

	extractor = FeatureExtractor(libpath)
	extactor_gain=1.0

	detector = AudioRecognition(libpath,graph,labels)
	detector.SetSensitivity(sensitivity)

	bufsize = detector.GetInputDataSize()

	print("Audio Recognition Version: " + detector.GetVersionString())

	audio_stream.start()
	try:
		while(True):
			frame = audio_stream.read(bufsize*2,bufsize*2)
			if(not frame):
				time.sleep(0.01)
				continue

			features = extractor.signal_to_mel(frame,extactor_gain)

			prediction = detector.RunDetection(features)

			if(prediction):
				now = datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S")
				print(detector.GetPredictionLabel(prediction) + " " + now)
				os.system(play_command + " ./resources/ding.wav")

	except KeyboardInterrupt:
		print("Terminating")
		audio_stream.stop()
		sys.exit(0)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--graph', type=str,
		default='../models/Hotword/sheila_small_0.3.tflite',
		help='Model to use for identification.')

	parser.add_argument(
		'--libpath', type=str,
		default=default_libpath,
		help='Path to Platform specific nyumaya_lib.')

	parser.add_argument(
		'--labels', type=str,
		default='../models/Hotword/sheila_labels.txt',
		help='Path to file containing labels.')

	parser.add_argument(
		'--sens', type=float,
                default='0.5',
		help='Sensitivity for detection. A lower value means more sensitivity, for example,'
		     '0.1 will lead to less false positives, but will also be harder to trigger.'
		     '0.9 will make it easier to trigger, but lead to more false positives')

	FLAGS, unparsed = parser.parse_known_args()

	label_stream(FLAGS.labels,FLAGS.libpath, FLAGS.graph, FLAGS.sens)
