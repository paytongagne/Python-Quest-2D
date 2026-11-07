"""Analyze recorded frame-work samples (microseconds) in JSON, no pygame required.
JSON accepts {"frame_us": [..]} or a numeric array. Does not measure anything itself.
"""
import argparse,json,math,statistics,sys
from pathlib import Path

def quantile(xs,p):
    xs=sorted(xs)
    return xs[min(len(xs)-1,max(0,math.ceil(p*len(xs))-1))]

def summarize(raw):
    values=raw.get('frame_us') if isinstance(raw,dict) else raw
    if not isinstance(values,list) or not values:
        raise ValueError('nonempty frame_us list required')
    if any(isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or x<0 for x in values):
        raise ValueError('samples must be finite nonnegative microseconds')
    ms=[x/1000 for x in values]
    return {'count':len(ms),'median_ms':round(statistics.median(ms),4),'p95_ms':round(quantile(ms,.95),4),'p99_ms':round(quantile(ms,.99),4),'max_ms':round(max(ms),4),'p95_under_16_7_ms':quantile(ms,.95)<=16.7}

def main():
    p=argparse.ArgumentParser();p.add_argument('recording',type=Path);args=p.parse_args()
    try: print(json.dumps(summarize(json.loads(args.recording.read_text())),indent=2))
    except (ValueError,OSError,json.JSONDecodeError) as e:
        print('ERROR:',e,file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
