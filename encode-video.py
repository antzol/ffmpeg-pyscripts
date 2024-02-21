import argparse
import math
import os
import subprocess

from modules import probe, globals


class Encoder:
    counter = 0
    success_files = []
    failed_files = []

    def __init__(self, config):
        self.input = config.input
        self.output = config.output
        self.crf = config.crf
        self.scale = config.scale
        self.tune = config.tune

    def process(self):
        if not os.path.exists(self.input):
            print('ERROR: input directory does not exist.')
            return

        if not os.path.exists(self.output):
            os.makedirs(self.output)

        if os.path.isfile(self.input):
            self.process_file(self.input)
        else:
            self.process_directory(self.input)

    def process_directory(self, directory):
        print('Process directory', directory)
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            self.process_file(os.path.join(directory, file))

    def process_file(self, file):
        cmd = [globals.__FFMPEG__, '-y']
        cmd.extend(['-i', file])

        if self.scale:
            cmd.extend(['-vf', 'scale={scale}'.format(scale=self.scale)])

        x265_params = 'strong-intra-smoothing=0:rect=0:aq-mode=1:rd=4:psy-rd=0.75:psy-rdoq=4.0:rdoq-level=1:rskip=2'
        video_args = ['-map', '0:V',
                      '-c:V:0', 'libx265',
                      '-vtag', 'hvc1',
                      '-crf', str(self.crf),
                      '-preset', 'slow']
        if self.tune:
            video_args.extend(['-tune', self.tune])
        video_args.extend(['-x265-params', x265_params])

        cmd.extend(video_args)

        audio_args = ['-map', '0:a', '-c:a', 'copy']
        subs_args = ['-map', '0:s', '-c:s', 'copy']
        metadata_args = ['-map_metadata:g', '0:g']
        format_args = ['-f', 'matroska']

        try:
            self.counter += 1
            print('\nTask #{num}: {file}'.format(num=self.counter, file=file))

            streams_info = probe.get_streams(file)
            if probe.contains_audio(streams_info):
                cmd.extend(audio_args)
            if probe.contains_subtitles(streams_info):
                cmd.extend(subs_args)
            cmd.extend(metadata_args)
            cmd.extend(format_args)

            output_file = os.path.splitext(os.path.basename(file))[0] + '.mkv'
            cmd.append(os.path.join(self.output, output_file))

            print('Start encoding...')
            subprocess.run(cmd, check=True)

            self.success_files.append(file)

        except subprocess.CalledProcessError as err:
            print("ERROR: subprocess returned a non-zero exit status")
            print("- cmd:", err.cmd)
            print("- return code:", err.returncode)
            print("- stdout:", err.stdout)
            print("- stderr:", err.stderr)

        except subprocess.TimeoutExpired as err:
            print("ERROR: subprocess timeout")
            print("- cmd:", err.cmd)
            print("- timeout:", err.timeout)
            print("- stdout:", err.stdout)
            print("- stderr:", err.stderr)

        except subprocess.SubprocessError:
            print("ERROR: unknown subprocess error")
            self.failed_files.append(file)

        except KeyboardInterrupt:
            print("ERROR: the processing was interrupted manually")
            self.failed_files.append(file)

    def print_results(self):
        print('\nResults:')
        if len(self.success_files):
            print('- successfully processed:')
            width = math.floor(math.log10(len(self.success_files))) + 1
            cnt = 0
            for file in self.success_files:
                cnt += 1
                print('  {cnt}. {file}'.format(cnt=str(cnt).zfill(width), file=file))
        if len(self.failed_files):
            print('- failed:')
            width = math.floor(math.log10(len(self.failed_files))) + 1
            cnt = 0
            for file in self.failed_files:
                cnt += 1
                print('  {cnt}. {file}'.format(cnt=str(cnt).zfill(width), file=file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='encode-video',
                                     description='''Creates an mkv file from H.265 encoded video and 
                                     copies of other elementary streams from the source file.''',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  help='Input directory or file',
                        default='C:/videoconv/input/')
    parser.add_argument('-o', '--output', help='Output directory',
                        default='C:/videoconv/output/')
    parser.add_argument('--preset',
                        choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium',
                                 'slow', 'slower', 'veryslow', 'placebo'],
                        help='The preset determines compression efficiency and therefore affects encoding speed.',
                        default='slow')
    parser.add_argument('--crf',
                        help='Constant rate factor (the lower CRF, the higher the video quality)',
                        type=int, default=22)
    parser.add_argument('--scale', help='''Resolution parameters of the output video.
    They are set in the format "width:height" (for example, "1920:1080").
    Any of these parameters can be set as -1 for automatic calculation (for example, "1920:-1").
    If this option is not specified, the resolution does not change.''',
                        required=False)
    parser.add_argument('--tune',
                        choices=['film', 'animation', 'grain', 'stillimage', 'fastdecode', 'zerolatency',
                                 'psnr', 'ssim'],
                        help='Settings based upon the specifics of your input. By default, it is disabled.',
                        required=False)
    args = parser.parse_args()

    encoder = Encoder(args)
    encoder.process()
    encoder.print_results()
