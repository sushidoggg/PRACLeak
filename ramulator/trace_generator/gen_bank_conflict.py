def generate_file(num_banks=8, filename="bank_conf.trace"):
    with open(filename, "w") as f:
        for i in range(num_banks):
            addr = i << 13
            f.write(f"0 {addr}\n")

if __name__ == "__main__":
    generate_file()
    print("Done.")
