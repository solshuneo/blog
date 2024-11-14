import subprocess
import os

def run_test_cases():
    for k in range(0, 35):
        # Đặt tên file inp và out tương ứng
        inp_filename = f"test/test{k+1}.inp"
        out_filename = f"test/test{k+1}.out"
        
        # Kiểm tra file .inp có tồn tại không
        if os.path.exists(inp_filename):
            # Gọi chương trình sol.exe với đầu vào từ file .inp
            with open(inp_filename, 'r') as inp_file:
                with open(out_filename, 'w') as out_file:
                    # Chạy sol.exe với file inp và ghi kết quả ra file out
                    subprocess.run(["dist/sol.exe"], stdin=inp_file, stdout=out_file)
            print(f"Test case {k+1} run, output written to {out_filename}")
        else:
            print(f"Input file {inp_filename} not found!")

if __name__ == "__main__":
    run_test_cases()
