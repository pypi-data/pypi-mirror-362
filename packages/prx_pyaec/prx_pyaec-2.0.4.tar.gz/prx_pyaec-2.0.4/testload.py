from prx_pyaec import Aec

@staticmethod
def main():
    # create an aex object
    frame_size = 1024
    filter_length = int(frame_size * 0.4)
    input_sample_rate = 16000
    print("calling Aec")
    aec = Aec(frame_size, filter_length, input_sample_rate, True)
    print("got aec, calling reset")
    aec.reset()
    print("got reset, calling del")
    del aec

if __name__ == "__main__":
    """The main entry point for running the prx_client"""
    main()
