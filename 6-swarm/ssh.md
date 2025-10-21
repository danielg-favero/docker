# Connect to the Manager Node
```bash
ssh -i "aws.pem" ec2-user@ec2-34-226-195-38.compute-1.amazonaws.com
```

# Connect to Node 1
```bash
ssh -i "aws.pem" ec2-user@ec2-54-91-208-234.compute-1.amazonaws.com
```

# Connect to Node 2
```bash
ssh -i "aws.pem" ec2-user@ec2-54-145-226-124.compute-1.amazonaws.com
```

# Join a node to Swarm
```bash
docker swarm join --token SWMTKN-1-0bx0uro5uegjqud620i3a40lj2uqxfirnfcfujjdco8yv6oazi-3df89q2qvgvntvxoj4rqivwlj 172.31.19.222:2377
```