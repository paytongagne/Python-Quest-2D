# Uses the authoring helpers; no learner code is executed.
from author_expeditions import task,case,ROOT,put
import json
task("titan_cloud",1,"Open the Cloud Link","Packets arrive in fragments. Restore the offline ingress conveyor.","A length prefix tells a decoder how many characters belong to the next message. Keep incomplete data for the next call.","Join the ASCII chunks. Decode decimal-length:payload frames. Return {'messages': [...], 'pending': remainder}. All prefixes are nonnegative decimal integers.","['3:a','bc0:2:x'] -> {'messages':['abc',''],'pending':'2:x'}","decode_frames(chunks)","Find ':', parse the length, and stop without consuming data when the payload is incomplete.",[
case([["3:a","bc0:2:x"]],{"messages":["abc",""],"pending":"2:x"}),case([[]],{"messages":[],"pending":""}),
case([["1:A1:B"]],{"messages":["A","B"],"pending":""}),case([["12"]],{"messages":[],"pending":"12"})],"""    buffer = ''.join(chunks)
    messages = []
    while ':' in buffer:
        index = buffer.index(':')
        size = int(buffer[:index])
        end = index + 1 + size
        if len(buffer) < end:
            break
        messages.append(buffer[index+1:end])
        buffer = buffer[end:]
    return {'messages':messages,'pending':buffer}""")
task("titan_cloud",2,"Reject Broken Telemetry","Bad capsules must be quarantined before the exchange accepts them.","Validate types before values. bool is an int subclass, so use type(value) is int when the contract excludes booleans.","Return sorted error names for missing or invalid fields: 'id' must be a nonempty str; 'seq' an int >=0 excluding bool; 'value' int/float excluding bool. Ignore extras.","{'id':'x','seq':True,'value':2} -> ['seq']","validate_frame(frame)","Use type() checks and combine missing and invalid cases into one error per field.",[
case([{"id":"A","seq":0,"value":2}],[]),case([{}],["id","seq","value"]),case([{"id":"","seq":True,"value":False}],["id","seq","value"]),case([{"id":"A","seq":-1,"value":3.5,"extra":0}],["seq"])],"""    errors = []
    if type(frame.get('id')) is not str or not frame['id']:
        errors.append('id')
    if type(frame.get('seq')) is not int or frame['seq'] < 0:
        errors.append('seq')
    if type(frame.get('value')) not in (int,float):
        errors.append('value')
    return errors""")
task("titan_cloud",3,"Subscribe to the Right Topic","The exchange must deliver a packet only to matching lanes.","Split topic paths by '/'. '+' matches exactly one level; a final '#' matches zero or more levels.","Return the indices of subscription patterns matching topic. '#' appears only as the last level. '+' occupies a whole level.","patterns=['lab/+','lab/#'], topic='lab/temp' -> [0,1]","subscribers(patterns, topic)","Compare each level. A final # accepts the rest; otherwise all levels must match.",[
case([["lab/+","lab/#","other"],"lab/temp"],[0,1]),case([["lab/#","lab/+"],"lab"],[0]),
case([["a/+/c","a/#","a/b"],"a/b/c"],[0,1]),case([[],"x"],[])],"""    result = []
    parts = topic.split('/')
    for index, pattern in enumerate(patterns):
        levels = pattern.split('/')
        matched = True
        for i, name in enumerate(levels):
            if name == '#':
                break
            if i >= len(parts) or (name != '+' and name != parts[i]):
                matched = False
                break
        else:
            matched = len(levels) == len(parts)
        if matched:
            result.append(index)
    return result""")
task("titan_cloud",4,"Know the Delivery Contract","Checkpoint the exchange before a storm retransmits old packets.","An idempotent consumer can filter repeated IDs even when delivery retries occur. Policy must be explicit.","Mode 'at_most_once' returns unique IDs in first-seen order. Mode 'at_least_once' preserves every arrival. Inputs use these two modes.","['A','A','B'], 'at_most_once' -> ['A','B']","deliver(ids, mode)","Use a seen set only when duplicates must be removed.",[
case([["A","A","B"],"at_most_once"],["A","B"]),case([["A","A"],"at_least_once"],["A","A"]),case([[],"at_most_once"],[]),case([["B","A","B","C"],"at_most_once"],["B","A","C"])],"""    if mode == 'at_least_once':
        return list(ids)
    return list(dict.fromkeys(ids))""")
task("helix_bio",1,"Draw the Synthetic Heartbeat","ION: This fictional lab uses a repeating toy pulse to test display software.","A discrete periodic model repeats a small template. Modulo gives the position within the period. These values are synthetic test units.","Return n samples by repeating [0, 0.1, -0.2, 1.0, -0.3, 0.2, 0.1, 0]. n is a nonnegative integer.","n=3 -> [0, 0.1, -0.2]","toy_pulse(n)","The sample at i is template[i % len(template)].",[
case([40],[0,.1,-.2,1.,-.3,.2,.1,0]*5),case([0],[]),case([3],[0,.1,-.2]),case([9],[0,.1,-.2,1.,-.3,.2,.1,0,0])],"""    template=[0,0.1,-0.2,1.0,-0.3,0.2,0.1,0]
    return [template[i % len(template)] for i in range(n)]""")
task("helix_bio",2,"Set the Sample Clock","The toy waveform must scroll against an exact millisecond clock.","A sample rate in Hz counts samples per second. Milliseconds per sample are 1000 / rate. Avoid repeated addition drift by multiplying the index.","Return n timestamps i*1000/rate_hz, starting at 0. Return [] when n<=0 or rate_hz<=0.","3 samples at 250 Hz -> [0,4,8]","timestamps(n, rate_hz)","Validate the rate before dividing. Compute each sample time from its index.",[
case([5,250],[0,4,8,12,16]),case([0,100],[]),case([3,0],[]),case([4,200],[0,5,10,15])],"""    if n <= 0 or rate_hz <= 0:
        return []
    return [i*1000/rate_hz for i in range(n)]""")
task("helix_bio",3,"Find Baseline Wander","The test rig added a linear trend. Estimate it from known calibration endpoints.","A line between first and last samples has slope (last-first)/(n-1). This toy exercise assumes endpoints contain only baseline.","Return the linearly interpolated baseline across the input length. Empty -> []; one sample -> that sample.","[2,9,4] -> [2,3,4]","baseline(samples)","Treat lengths zero and one separately, then interpolate between endpoints.",[
case([[2,9,4]],[2,3,4]),case([[]],[]),case([[7]],[7]),case([[0,8,9,3]],[0,1,2,3])],"""    if len(samples) < 2:
        return list(samples)
    return [samples[0]+i*(samples[-1]-samples[0])/(len(samples)-1) for i in range(len(samples))]""")
noise=lambda samples,seed,amp: [round(v+(((seed+i*17)%101)/50-1)*amp,6) for i,v in enumerate(samples)]
task("helix_bio",4,"Inject Noise for Testing","Stress the display with a repeatable synthetic perturbation. No patient measurements are used.","A specified index formula makes every test reproducible. Returning a new list keeps the original fixture usable.","At index i add (((seed+i*17)%101)/50 - 1)*amplitude. Round each result to 6 decimals. Preserve the input.","[0,0], seed=0, amplitude=1 -> [-1,-0.66]","inject_noise(samples, seed, amplitude)","Enumerate the input and apply the formula to each sample.",[
case([[0,.1,-.2,1,-.3,.2,.1,0]*3,7,.15],noise([0,.1,-.2,1,-.3,.2,.1,0]*3,7,.15)),
case([[],1,2],[]),case([[1,2],0,0],[1,2]),case([[0,0],0,1],[-1,-.66])],"""    return [round(v+(((seed+i*17)%101)/50-1)*amplitude,6) for i,v in enumerate(samples)]""")
task("aurora_ep",1,"Represent a Mapping Sample","The observatory plots fictional measurements on a toy chamber.","Keep geometry and scalar metadata together in a record. Dictionaries give each field an explicit meaning.","Return {'position': point, 'voltage': voltage, 'time_ms': time_ms}. point contains three coordinates in toy units.","point=[1,0,0], voltage=2, time=5 -> labeled sample record","mapping_sample(point, voltage, time_ms)","Copy the point into the position field and label the two scalars.",[
case([[1,0,0],2,5],{"position":[1,0,0],"voltage":2,"time_ms":5}),
case([[0,-1,2],0,0],{"position":[0,-1,2],"voltage":0,"time_ms":0})],"""    return {'position':list(point),'voltage':voltage,'time_ms':time_ms}""")
task("aurora_ep",2,"Smooth the Catheter Path","Move the simulated catheter marker between two recorded positions.","Linear interpolation is a + (b-a)*t for each coordinate. Clamp t when the simulation is outside its interval.","Return three interpolated coordinates between a and b. Clamp t to [0,1]. All geometry is fictional.","a=[0,0,0], b=[2,4,6], t=.5 -> [1,2,3]","cursor_position(a, b, t)","Clamp the fraction, then zip the coordinates and interpolate each axis.",[
case([[0,0,0],[2,4,6],.5],[1,2,3]),case([[1,2,3],[4,5,6],-1],[1,2,3]),
case([[1,2,3],[4,5,6],2],[4,5,6]),case([[0,0,0],[0,0,0],.3],[0,0,0])],"""    t=max(0,min(1,t))
    return [x+(y-x)*t for x,y in zip(a,b)]""")
task("aurora_ep",3,"Translate Reference Frames","The chamber and cursor use different coordinate origins. Apply a documented transform.","Multiply a point by the 3x3 rotation matrix, then add the translation. Each output component is a row dot product.","Return R*point + translation as a three-element list. All fixtures use a 3x3 matrix.","A quarter-turn about z maps [1,0,0] to [0,1,0].","transform(point, rotation, translation)","For each row sum rotation[i][j]*point[j], then add translation[i].",[
case([[1,0,0],[[0,-1,0],[1,0,0],[0,0,1]],[2,0,0]],[2,1,0]),
case([[1,2,3],[[1,0,0],[0,1,0],[0,0,1]],[0,0,0]],[1,2,3]),
case([[0,0,0],[[1,0,0],[0,1,0],[0,0,1]],[-1,2,0]],[-1,2,0])],"""    return [sum(rotation[i][j]*point[j] for j in range(3))+translation[i] for i in range(3)]""")
task("aurora_ep",4,"Reject Bad Mapping Points","The display must distinguish reliable samples from bad contact.","Filter records using explicit quality metadata. These thresholds are game rules, with no diagnostic meaning.","Return the IDs of samples with contact True and confidence >= 0.8. Missing fields fail. Preserve order.","[{'id':'a','contact':True,'confidence':.9}] -> ['a']","accepted_samples(samples)","Use get for optional fields. Require contact is True and a numeric confidence.",[
case([[{"id":"A","contact":True,"confidence":.9},{"id":"B","contact":False,"confidence":1},{"id":"C","contact":True,"confidence":.8}]],["A","C"]),
case([[]],[]),case([[{"id":"x"},{"id":"y","contact":True,"confidence":.79}]],[])],"""    return [s['id'] for s in samples if s.get('contact') is True and s.get('confidence',0)>=0.8]""")
# Each destination has a proper navigable four-station landscape with return shuttle.
for zone in ("titan_cloud","helix_bio","aurora_ep"):
    p=ROOT/"planets"/(zone+".json")
    m=json.loads(p.read_text())
    m["interactables"]=[dict(type="terminal",challenge_id=f"{zone}_{i:02}",x=x,y=y) for i,(x,y) in enumerate([(300,220),(800,180),(800,600),(260,580)],1)]
    put("planets",zone,m)

