resource "aws_codestarconnections_connection" "mygithub" {
  name          = "mygithub"
  provider_type = "GitHub"
}




resource "aws_codepipeline" "djangoCodePipeline" {
  name = "djangoCodePipeline"
  role_arn = aws_iam_role.codepipeline_role2.arn

  artifact_store {
    location = aws_s3_bucket.bucket.bucket
    type = "S3"
  }

  stage {
    name = "Source"

    action {
      name = var.resource_tag_name
      category = var.category
      owner = var.owner
      provider = "GitHub"
      version = "1"
      output_artifacts = ["SourceArtifact"]

      configuration = {
        OAuthToken = var.github_token
        Owner = var.github_owner
        Repo = var.github_repo
        Branch = var.branch
      }
    }
  }


  stage {
    name = "Deploy_to_EC2"

    action {
      name = "codeDeploy"
      category = "codeDeploy"
      owner = "AWS"
      provider = "CodeDeploy"
      input_artifacts = ["SourceArtifact"]
      version = "1"

      configuration = {
      ApplicationName    = aws_codedeploy_app.djangodeploy.name 
      DeploymentGroupName = aws_codedeploy_deployment_group.djangodeploy.deployment_group_name  
    }
    }
  }
  stage {
    name = "Deploy_to_S3"

    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "S3"
      input_artifacts = ["SourceArtifact"]
      version         = "1"
 
      configuration = {
        BucketName = aws_s3_bucket.bucket.bucket
        Extract = "true"
      }
    }
  }
}
