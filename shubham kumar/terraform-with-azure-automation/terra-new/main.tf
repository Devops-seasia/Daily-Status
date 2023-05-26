terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.56.0"
    }
  }
  backend "azurerm" {
      resource_group_name  = "terra-rg"
      storage_account_name = "tfstatebackup999"
      container_name       = "mytfstatefile"
      key                  = "tiger.tfstate"
  }
}

provider "azurerm" {
  features {} 
}


variable "prefix" {
  default = "tiger"
}

resource "azurerm_resource_group" "example" {
  name     = "${var.prefix}-resources"
  location = "Australia East"
}

resource "azurerm_network_security_group" "my-sg" {
    name = "sg"
    location = azurerm_resource_group.example.location
    resource_group_name = azurerm_resource_group.example.name
    security_rule {
    name                       = "test100"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "test150"
    priority                   = 150
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "test200"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  
}
resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]

}
resource "azurerm_network_interface_security_group_association" "ngs-association" {
  network_interface_id = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.my-sg.id

}
resource "azurerm_network_interface" "main" {
  name                = "${var.prefix}-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = azurerm_public_ip.example.id
  }
}
resource "azurerm_public_ip" "example" {
  name                = "acceptanceTestPublicIp1"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  allocation_method   = "Static"
}
resource "azurerm_virtual_machine" "main" {
  name                  = "${var.prefix}-vm"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.main.id]
  vm_size               = "Standard_DS1_v2"
  

  ############################## Uncomment this line to delete the OS disk automatically when deleting the VM
  ###################################### delete_os_disk_on_termination = true

  ########################################## Uncomment this line to delete the data disks automatically when deleting the VM
  ################################### delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "tiger-vm"
    admin_username = "kosta"
    admin_password = "Shubham@12345"
    custom_data = filebase64("./script.sh")
  }
  os_profile_linux_config {
    disable_password_authentication = false
  }
  tags = {
    environment = "staging"
  }
}

resource "null_resource" "delay" {
  provisioner "local-exec" {
    command = <<EOT
      ping 127.0.0.1 -n 151 > nul
    EOT
    interpreter = ["cmd", "/C"]
  }
}
resource "azurerm_managed_disk" "example" {
  name                 = "managed-disk"
  location             = azurerm_resource_group.example.location
  resource_group_name  = azurerm_resource_group.example.name
  storage_account_type = "Standard_LRS"
  create_option        = "Copy"
  disk_size_gb         = "30"
  source_resource_id = "/subscriptions/816a394a-c009-43b5-b198-ed5c03e9a05f/resourceGroups/tiger-resources/providers/Microsoft.Compute/disks/myosdisk1"
  depends_on = [ azurerm_virtual_machine.main ]
}

resource "azurerm_snapshot" "example" {
  name                = "snapshot"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  create_option       = "Copy"
  source_uri          = azurerm_managed_disk.example.id
}

resource "azurerm_image" "example" {
  name                = "acctest"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  os_disk {
    os_type  = "Linux"
    os_state = "Generalized"
    size_gb  = 30
    managed_disk_id = azurerm_managed_disk.example.id
  }
}

resource "azurerm_shared_image_gallery" "example" {
  name                = "example_image_gallery"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  description         = "Shared images and things."
}

resource "azurerm_shared_image" "example" {
  name                = "my-image"
  gallery_name        = azurerm_shared_image_gallery.example.name
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  os_type             = "Linux"

  identifier {
    publisher = "Kosta"
    offer     = "Offer"
    sku       = "Sku"
  }
}


resource "azurerm_shared_image_version" "example" {
  name                = "0.0.1"
  gallery_name        = azurerm_shared_image_gallery.example.name
  image_name          = azurerm_shared_image.example.name
  resource_group_name = azurerm_shared_image.example.resource_group_name
  location            = azurerm_shared_image.example.location
  managed_image_id    = azurerm_image.example.id

  target_region {
    name                   = azurerm_shared_image.example.location
    regional_replica_count = 2
    storage_account_type   = "Standard_LRS"
  }
}

###############################################################################################
resource "azurerm_public_ip" "lb-ip" {
  name                = "my-lb-ip"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  allocation_method   = "Static"

  tags = {
    environment = "Production"
  }
}

resource "azurerm_lb" "example" {
  name                = "example-lb"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  frontend_ip_configuration {
    name                          = "PublicIPAddress"
    public_ip_address_id          = azurerm_public_ip.lb-ip.id
  }
}

resource "azurerm_lb_probe" "example" {
  name                = "healthProbe"
  loadbalancer_id     = azurerm_lb.example.id
  protocol            = "Tcp"
  port                = 80
  interval_in_seconds = 15
  number_of_probes    = 2
}

resource "azurerm_lb_backend_address_pool" "example" {
  loadbalancer_id     = azurerm_lb.example.id
  name                = "backendPool"
}

resource "azurerm_lb_rule" "example" {
  name                           = "example-rule"
  loadbalancer_id                = azurerm_lb.example.id
  frontend_ip_configuration_name = azurerm_lb.example.frontend_ip_configuration[0].name
  frontend_port                  = 80
  backend_port                   = 80
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.example.id]
  probe_id                       = azurerm_lb_probe.example.id
  protocol                       = "Tcp"
  enable_floating_ip             = false
  load_distribution              = "Default"
  idle_timeout_in_minutes        = 15
}
# ####################################################################################

resource "azurerm_virtual_network" "vmss-vnet" {
  name                = "vmss-vnet"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "vmss-subnet" {
  name                 = "vmss-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.vmss-vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_network_security_group" "vmss-nsg" {
  name                = "vmss-nsg"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
}

resource "azurerm_subnet_network_security_group_association" "example" {
  subnet_id                 = azurerm_subnet.vmss-subnet.id
  network_security_group_id = azurerm_network_security_group.vmss-nsg.id
}

######################################################################################################
# Create a virtual machine scale set using the custom image

resource "azurerm_virtual_machine_scale_set" "example" {
  name = "vmss-with-linuxs"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  depends_on = [ azurerm_shared_image_version.example ]

  sku {
    name     = "Standard_DS1_v2"
    capacity = 1
  }
  
  storage_profile_image_reference {
   id = "/subscriptions/816a394a-c009-43b5-b198-ed5c03e9a05f/resourceGroups/tiger-resources/providers/Microsoft.Compute/galleries/example_image_gallery/images/my-image/versions/0.0.1"
  }
  storage_profile_os_disk {
    managed_disk_type = "Standard_LRS"
    name              = ""
    create_option     = "FromImage"
  }
 
  os_profile {
    computer_name_prefix = "linux-vmss"
    admin_username       = "kosta"
    admin_password       = "Shubham@12345"
  }
  
  upgrade_policy_mode = "Automatic"

  network_profile {
    name    = "example-nic"
    primary = true

    ip_configuration {
      name                          = "example-ipconfig"
      subnet_id                     = azurerm_subnet.internal.id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.example.id]
      primary = true
    }
    network_security_group_id = azurerm_network_security_group.my-sg.id
  }
}

################################################################################

resource "azurerm_monitor_autoscale_setting" "example" {
  name                = "myAutoscaleSetting"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  target_resource_id  = azurerm_virtual_machine_scale_set.example.id

  profile {
    name = "defaultProfile"

    capacity {
      default = 1
      minimum = 1
      maximum = 3
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_virtual_machine_scale_set.example.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 75
        metric_namespace   = "microsoft.compute/virtualmachinescalesets"
        dimensions {
          name     = "AppName"
          operator = "Equals"
          values   = ["App1"]
        }
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT1M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "Percentage CPU"
        metric_resource_id = azurerm_virtual_machine_scale_set.example.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 25
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = 1
        cooldown  = "PT1M"
      }
    }
  }

  notification {
    email {
      send_to_subscription_administrator    = true
      send_to_subscription_co_administrator = true
      custom_emails                         = ["shubham69812@gmail.com"]
    }
  }
}