class AuthorizedKeys:
    USERDATA = """

cat > /home/ubuntu/.ssh/authorized_keys << EOF
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAGxlZsduAGeKqz3UhzHeXiJOsRlBQTZIyOxA0DrXso9ncD\
veooDqUr+Xw5XZx44nHFNjWocoQowDdaA8jj0DYEs9wF5ELGj/rm4n6a1b6tXVAlb3Vojb5C0mZfx2gUA6i5GNnNXONRttaW53XeOoD/VDM9tlgBnpa04bB\
Q1naTiLbQsQg== os@controller
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAFJ/TSfJegktNbVbCF2L1hte8qfDtgk/zArlNq4vgEAKRe\
PSEYnoFldlGVn5zDqnvLP2xy6WrcFUjO2TOeTnmqQ1gEzcBOjUXeYdA7LO1J8yARvvAMOk4IiuVTvGUdCIW8uDpXwfqCxqeKbSudo3LVLgt/ZcRg1QENyRL\
P/zqixIJoEsA== os@compute01
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACnHtnIvTXuTG2I5ngNXKUYu/h7izkEGPmfZpqIeuXcQIY\
0miX7k+9snBvPXKuxp5nYspOZuOzsHs4JEE3l/+ftcgHvF7w3SD5CtdTfGMhUwGHtcpWtKfj18+FiDwh9wK4m6exBChpfBTU1q14LPZBR7xg9KZULWGddug\
mffUK1SMoWdg== os@compute02
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACA0/h9uiML5XfA2zobZTkjZjUDfVBpwfqO1V76/+NLpwp\
HOVGNQPMYxfYcNaXI2HbXBTwXGkAaYq8w3s7WF+zN1QEldCkmHk3wLFWtxOq2UP+6UhnR0Li1FczZ//695A6j0BSm6CxiC+Q0J5BDih4eIjrJwKmAANYGz6\
yPzEPR/pj9VA== os@compute03.etit.tu-chemnitz.de
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAG6PCMQcMNvSA4yRmHETOYdj60fsJo4n8FOBKmlw2fJR7x\
WMND0DQWTVvPssv3bw1iKn5zLbx4aeVd7idKT00HsjwB4mX1/+UBVUeP/21tp50J3XsG5Pdwz4JL6LeRWvurKoU66bpBR5u0Iuo9VrJlHfn3GbCiHzke7uU\
t3QBmBWkxroQ== sdn@sdnc
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBACU7DStTMa4kHmnZ6kiNkQHrW4CYW9kOKkR8xQa3yBvPDG\
0IYv0MuUJg2lY5TfdhmXNWELPYHlZxieOC60HTD/vzACoV3268mlJNYGE+ju4iQq+QXaUSwog4YkQs4aDCpylyDRJYWFe8YP97/xFOzR5P5bxCYcJZQLlwW\
a/+294kW29hQ== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAEBCbxZcyGw+PD3S/HoPx/WKhfGOz4Mos3OGQ4Q2rvh7Up\
NBE4UVp/xOBcFoL0WveHI+WskQV0jKa7TnErjVwEsOAAX6O4DxaskATGq6XioPv2XmRGKb5UZ28NUCE+VLhUvnFLLn2IMiCSiNzCU8hX0rjsU6/hHjDyV01\
Iahq2gAY6E7Q== hanif@openstack
ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAHLT0AS5MHwwJ6hX1Up5stfz361+IWA/8/MhZBH+mYA32h/Bp5hSWkQDXow4aDiHRlxVV1WLlHHup+GPBBA9XLTRwHP8gAjbP5EM4EVxR9EbDh5Hz13xcN0/n9J9rasefHS8UgTJUgRrWeNRCSAhkbNfDfSeQzk8NWlzhiwwCIUacKnzg== hanif@kukkalli
EOF

echo "---------------------------------------------------"
echo "-------------- Added authorized keys --------------"
echo "---------------------------------------------------"

    """