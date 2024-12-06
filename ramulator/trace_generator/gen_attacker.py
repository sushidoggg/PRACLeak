def gen_flush_trace(base_addr, num_lines=16, filename="flush.trace"):
    with open(filename, "w") as f:
        for i in range(num_lines):
            addr = base_addr + 64 * i
            f.write(f"0 {addr}\n")

def get_addr_from_row(row, bank=17):
    addr = row
    addr <<= 12
    addr |= bank
    addr <<= 6
    return addr

def gen_full_monitor_trace(bank=17, filename="monitor.trace"):
    with open(filename, "w") as f:
        for row in range(1 << 16):
            addr = get_addr_from_row(row, bank=bank)
            f.write(f"127 {addr}\n")

def gen_verify_monitor_trace(base_addr, cutoff=4000, bank=17, num_lines=16,
                           filename="monitor_verify.trace"):
    with open(filename, "w") as f:
        for row in range(cutoff):
            addr = get_addr_from_row(row, bank=bank)
            f.write(f"127 {addr}\n")

        curr_row = cutoff
        for i in range(100):
            for j in range(num_lines):
                addr = base_addr + 64 * j
                f.write(f"127 {addr}\n")

                # dummy accesses to eliminate noise in observation
                for k in range(3):
                    addr = get_addr_from_row(curr_row)
                    curr_row += 1
                    f.write(f"127 {addr}\n")

# def gen_partial_monitor_trace()

if __name__ == "__main__":
    base_addr = 0x555555558040
    gen_flush_trace(base_addr)
    gen_full_monitor_trace()
    gen_verify_monitor_trace(base_addr)
    print("Done.")
