from django.db import models

# Create your models here.
class project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class task(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class comment(models.Model):
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.task.title}"
    
class attachment(models.Model):
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task.title}"
    
class project_member(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.member_name} - {self.role} in {self.project.name}"
    
class milestone(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    due_date = models.DateField()

    def __str__(self):
        return f"Milestone: {self.title} for {self.project.name}"
    
class time_log(models.Model):
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)
    log_date = models.DateField()

    def __str__(self):
        return f"{self.hours_spent} hours on {self.task.title}"