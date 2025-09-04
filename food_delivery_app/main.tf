# choosing the cloud service provider
provider "aws" {
  region = "us-west-2"
}
# creating variable for reusability
variable "name_vpc" {
  description = "The name of the VPC"
  type        = string
  default     = "food-delivery-vpc"
}
variable "cidr" {
    default = "10.0.0.0/16"
}
#creating resources
resource "aws_key_pair" "deployer" {
  key_name   = "aws_key"
  public_key = file("~/.ssh/F/quiggy_flask/aws_key.pub") # Replace with your public key path
}

resource "aws_vpc" "vpc" {
  cidr_block = var.cidr
}

resource aws_subnet "public_subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone = "us-west-2a"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "vpc_igw" {
  vpc_id = aws_vpc.vpc.id
}
resource "aws_route_table" "app_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc.id
  }
}
resource "aws_security_group" "app_sg" {
  name        = "app_sg"
  description = "Allow inbound traffic for app server"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow ssh"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
   }

resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  security_groups = module.vpc.default_security_group_ids
  key_name      = "aws_key" # Replace with your key pair name
  subnet_id     = aws_subnet.public_subnet.id
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/F/quiggy_flask/aws_key") # Replace with your private key path
    host        = self.public_ip  ## since i'm inside the instance already i'm using self or resource type.name.public_ip
  }
  

  # provisioner to copy the files from our local machine to the instance
  provisioner "file" {
    source      = "F:/quiggy_flask/food_delivery_app/app.py"
    destination = "/home/ubuntu/app"
    
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install python3-pip -y",
      "pip3 install flask",
      "cd/home/ubuntu",
      "sudo python3 app.py"
    ]
    
  }
}

 
