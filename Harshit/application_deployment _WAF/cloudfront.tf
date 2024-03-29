
resource "aws_cloudfront_distribution" "distribution" {
   web_acl_id = aws_wafv2_web_acl.fireballs.arn

##################this resource will attche firewall with cloudfront######################
  origin {
    domain_name = aws_s3_bucket.bucket.bucket_regional_domain_name
    origin_id   = "s3"

   ################conifigure cloud front with s3#######################3
    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols = ["TLSv1","TLSv1.1","TLSv1.2"]
    }
  }
  ###############configure loadbalancer with cloudfront############# 
  origin {
    domain_name = aws_lb.loadbalancer.dns_name
    origin_id = "lbattached"
  
  custom_origin_config {
    http_port = 80
    https_port = 443
    origin_protocol_policy = "http-only"
    origin_ssl_protocols = ["TLSv1","TLSv1.1","TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  # comment             = "Some comment"
  # default_root_object = "index.html"


  default_cache_behavior {
    allowed_methods  = ["HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "lbattached"
    

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

   # Cache behavior with precedence 0
  ordered_cache_behavior {
    path_pattern     = "index.html"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "s3"

    forwarded_values {
      query_string = false
      headers      = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    compress               = true
    viewer_protocol_policy = "allow-all"
  }

 price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "blacklist"
      locations        = ["US", "CA", "GB", "DE"]
    }
  }

 
  viewer_certificate {
    cloudfront_default_certificate = true
  }

}


