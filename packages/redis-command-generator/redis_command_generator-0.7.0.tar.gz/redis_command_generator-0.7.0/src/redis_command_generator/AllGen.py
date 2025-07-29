from simple_parsing import parse
from dataclasses import dataclass
from redis_command_generator.SetGen import SetGen
from redis_command_generator.ZSetGen import ZSetGen
from redis_command_generator.StringGen import StringGen
from redis_command_generator.StreamGen import StreamGen
from redis_command_generator.ListGen import ListGen
from redis_command_generator.HyperLogLogGen import HyperLogLogGen
from redis_command_generator.HashGen import HashGen
from redis_command_generator.GeoGen import GeoGen
from redis_command_generator.BitmapGen import BitmapGen
from redis_command_generator.TimeSeriesGen import TimeSeriesGen

@dataclass
class AllGen(SetGen, ZSetGen, StringGen, StreamGen, ListGen, HyperLogLogGen, HashGen, GeoGen, BitmapGen, TimeSeriesGen):
    pass

if __name__ == "__main__":
    all_dt_gen = parse(AllGen)
    all_dt_gen._run()
