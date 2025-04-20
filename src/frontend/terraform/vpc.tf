resource "aws_vpc" "loregen_front_vpc" {
  cidr_block = "10.50.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "loregen_front_dashboard_vpc_1"
  }
}

resource "aws_subnet" "loregen_front_dashboard_subnet_public_1a" {
  vpc_id            = aws_vpc.loregen_front_vpc.id
  cidr_block        = "10.50.1.0/24"
  availability_zone = "eu-central-1a"

  tags = {
    Name = "loregen_front_dashboard_public_1a"
  }
}

resource "aws_subnet" "loregen_front_dashboard_subnet_public_1b" {
  vpc_id            = aws_vpc.loregen_front_vpc.id
  cidr_block        = "10.50.2.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name = "loregen_front_dashboard_public_1b"
  }
}

resource "aws_subnet" "loregen_front_dashboard_subnet_private_1a" {
  vpc_id            = aws_vpc.loregen_front_vpc.id
  cidr_block        = "10.50.3.0/24"
  availability_zone = "eu-central-1a"

  tags = {
    Name = "loregen_front_dashboard_private_1a"
  }
}

resource "aws_subnet" "loregen_front_dashboard_subnet_private_1b" {
  vpc_id            = aws_vpc.loregen_front_vpc.id
  cidr_block        = "10.50.4.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name = "loregen_front_dashboard_private_1b"
  }
}

resource "aws_internet_gateway" "loregen_front_dashboard_igw" {
  vpc_id = aws_vpc.loregen_front_vpc.id

  tags = {
    Name = "loregen_front_dashboard_igw_1"
  }
}

resource "aws_eip" "nat_1a" {
}

resource "aws_nat_gateway" "nat_1a" {
  allocation_id = aws_eip.nat_1a.id
  subnet_id     = aws_subnet.loregen_front_dashboard_subnet_public_1a.id

  tags = {
    Name = "loregen_front_dashboard_nat_gw_1a"
  }
}

resource "aws_eip" "nat_1b" {
}

resource "aws_nat_gateway" "nat_1b" {
  allocation_id = aws_eip.nat_1b.id
  subnet_id     = aws_subnet.loregen_front_dashboard_subnet_public_1b.id

  tags = {
    Name = "loregen_front_dashboard_nat_gw_1b"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.loregen_front_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.loregen_front_dashboard_igw.id
  }

  tags = {
    Name = "loregen_front_dashboard_public_1x_rt"
  }
}

resource "aws_route_table" "private_rt_1a" {
  vpc_id = aws_vpc.loregen_front_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_1a.id
  }

  tags = {
    Name = "loregen_front_dashboard_private_1a_rt"
  }
}

resource "aws_route_table" "private_rt_1b" {
  vpc_id = aws_vpc.loregen_front_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_1b.id
  }

  tags = {
    Name = "loregen_front_dashboard_private_1b_rt"
  }
}

resource "aws_route_table_association" "loregen_front_dashboard_rta_public_1a" {
  subnet_id      = aws_subnet.loregen_front_dashboard_subnet_public_1a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "loregen_front_dashboard_rta_public_1b" {
  subnet_id      = aws_subnet.loregen_front_dashboard_subnet_public_1b.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "loregen_front_dashboard_rta_private_1a" {
  subnet_id      = aws_subnet.loregen_front_dashboard_subnet_private_1a.id
  route_table_id = aws_route_table.private_rt_1a.id
}

resource "aws_route_table_association" "loregen_front_dashboard_rta_private_1b" {
  subnet_id      = aws_subnet.loregen_front_dashboard_subnet_private_1b.id
  route_table_id = aws_route_table.private_rt_1b.id
}

