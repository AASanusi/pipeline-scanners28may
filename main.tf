provider "aws" { #provider plugin informing terraform it's aws is the provider used
  region = "eu-west-2" # region where this will be made and managed
}

resource "aws_s3_bucket" "iacmade28may" { #resource is s3 bucket and local name of bucket which can be referenced in code e.g aws_s3_bucket.iacmade28may
  bucket = "iacmade28may" #Name of the bucket in aws
}

#Setting up remote state backend - backend stoted in s3 (as storage resource) and it's where tfstate will be stored. Ensuring local backend and remote backend availble.
terraform { #Terrform code to start configuring backend or for version settings
  backend "s3" { # backend block to s3
    bucket = "iacmade28may" #Bucket where tfstate will be stored
    key = "global/s3/terraform.tfstate" #path of where terraform statefile will be in the bucket. If you go on aws you can follow this.
    region = "eu-west-2" # region it will be stored in
  }
}

# Remember need to first build bucket first before building the remote backend state for it otherwise will get an error saying backend doens't exists. Once created bucket - will need to add backend and initialise again. - Evertime you make changes either remove or add you will need to INITIALISE as it sets the correct state for terraform. This is it as git - git add, git commit, git push - only if it had git status where I can check if I need to initialise or not.

# Terraform declarative language meaning that it sets the final state you want it to be in. Terraform is agnostic meaning it works/compatable with numerous 'provider' e.g docker,aws, azure

# Once you create the bucket - you'll notice on local machine of left hand side the local statefile created - meaning remote needs to be created to to keep track of each states. ANd finally once migrated local backend to new s3 remote backend, terraform.tfstate.backup appears - ensuring both backend have been linked.

# Use same name for remote statefile as local state file when creatung the 'key' path for it in your aws bucket e.g terraform.tfstae