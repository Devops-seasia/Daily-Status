variable "cluster-name" {
  default = "terraform-eks-demo"
  type    = string
}






resource "aws_iam_role" "eks-demo-cluster-iam" {
  name = "eks-demo-cluster-iam"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "eks-demo-cluster-iam-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks-demo-cluster-iam.name
}

resource "aws_iam_role_policy_attachment" "eks-demo-cluster-iam-AmazonEKSServicePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.eks-demo-cluster-iam.name
}

resource "aws_security_group" "eks-demo-cluster-sg" {
  name        = "terraform-eks-demo-cluster"
  description = "Cluster communication with worker nodes"
  vpc_id      = aws_vpc.my_vpc.id

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "terraform-eks-demo"
  }
}




resource "aws_eks_cluster" "eks-demo-cluster" {
  name     = var.cluster-name
  role_arn = aws_iam_role.eks-demo-cluster-iam.arn

  vpc_config {
    security_group_ids = [aws_security_group.eks-demo-cluster-sg.id]
    subnet_ids    = [
    aws_subnet.public_subnet_1.id,
    aws_subnet.private_subnet_2.id,
    aws_subnet.public_subnet_3.id
  ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks-demo-cluster-iam-AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.eks-demo-cluster-iam-AmazonEKSServicePolicy,
  ]
}