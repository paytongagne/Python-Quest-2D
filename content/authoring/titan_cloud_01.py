def decode_frames(chunks):
    buffer = ''.join(chunks)
    messages = []
    while ':' in buffer:
        index = buffer.index(':')
        size = int(buffer[:index])
        end = index + 1 + size
        if len(buffer) < end:
            break
        messages.append(buffer[index+1:end])
        buffer = buffer[end:]
    return {'messages':messages,'pending':buffer}
