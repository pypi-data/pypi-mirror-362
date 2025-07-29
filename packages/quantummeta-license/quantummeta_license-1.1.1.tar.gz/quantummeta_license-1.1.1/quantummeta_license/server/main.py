#!/usr/bin/env python3
"""
FastAPI License Server - Main Application
Real license server with email delivery to bajpaikrishna715@gmail.com
"""

import os
import json
import smtplib
import uuid
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Request, Form, File, UploadFile, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import uvicorn

from ..core.license_manager import LicenseManager
from ..core.hardware import get_machine_id
from ..core.validation import validate_or_grace

# Initialize FastAPI app
app = FastAPI(
    title="QuantumMeta License Server",
    description="Secure license generation and management server",
    version="1.1.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
LICENSE_DB = {}
REQUEST_DB = {}
ADMIN_EMAIL = "bajpaikrishna715@gmail.com"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

# Pydantic models
class LicenseRequest(BaseModel):
    email: EmailStr
    package_name: str
    intended_use: str
    machine_id: Optional[str] = None

class LicenseValidation(BaseModel):
    license_data: str
    machine_id: Optional[str] = None

class AdminLogin(BaseModel):
    email: EmailStr
    token: str

# Helper functions
def send_email(to_email: str, subject: str, body: str, attachment_path: Optional[str] = None):
    """Send email with optional attachment"""
    try:
        if not EMAIL_PASSWORD:
            raise Exception("Email password not configured")
            
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(ADMIN_EMAIL, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(ADMIN_EMAIL, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def generate_license_file(request_data: dict, license_id: str) -> str:
    """Generate actual license file using the existing system"""
    try:
        license_manager = LicenseManager()
        
        # Create temporary license file
        license_path = f"temp_license_{license_id}.qkey"
        
        # Generate license using the existing system
        license_data = license_manager.create_license(
            package_name=request_data["package_name"],
            user_email=request_data["email"],
            features=["core", "pro"],
            validity_days=365,
            machine_id=request_data.get("machine_id"),
            additional_data={"intended_use": request_data["intended_use"]}
        )
        
        # Save license file
        license_manager.save_license(license_data, license_path)
        
        return license_path
    except Exception as e:
        print(f"License generation error: {e}")
        return None

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with license request form"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QuantumMeta License Server</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ text-align: center; color: white; margin-bottom: 30px; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
            .form-container {{ background: white; border-radius: 15px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            .form-group {{ margin-bottom: 20px; }}
            .form-group label {{ display: block; margin-bottom: 8px; font-weight: 600; color: #555; }}
            .form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 12px; border: 2px solid #e1e5e9; border-radius: 8px; font-size: 14px; }}
            .btn {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; width: 100%; }}
            .btn:hover {{ transform: translateY(-2px); }}
            .packages {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
            .package {{ background: #f8f9fa; border: 2px solid #e1e5e9; border-radius: 8px; padding: 15px; text-align: center; cursor: pointer; }}
            .package.selected {{ border-color: #667eea; background: #e3f2fd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 QuantumMeta License Server</h1>
                <p>Request licenses for premium AI, Quantum, and AGI packages</p>
            </div>
            
            <div class="form-container">
                <h2>Request License</h2>
                <form id="licenseForm" onsubmit="submitRequest(event)">
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Select Package</label>
                        <div class="packages">
                            <div class="package" onclick="selectPackage('quantum-metalearn')">
                                <h4>quantum-metalearn</h4>
                                <p>Advanced ML algorithms</p>
                            </div>
                            <div class="package" onclick="selectPackage('se-agi')">
                                <h4>se-agi</h4>
                                <p>Software Engineering AGI</p>
                            </div>
                            <div class="package" onclick="selectPackage('kyber-pqc')">
                                <h4>kyber-pqc</h4>
                                <p>Post-quantum cryptography</p>
                            </div>
                            <div class="package" onclick="selectPackage('neural-quantum')">
                                <h4>neural-quantum</h4>
                                <p>Quantum neural networks</p>
                            </div>
                        </div>
                        <input type="hidden" id="package_name" name="package_name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="intended_use">Intended Use</label>
                        <textarea id="intended_use" name="intended_use" rows="3" placeholder="Describe how you plan to use this package" required></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="machine_id">Machine ID (Optional)</label>
                        <input type="text" id="machine_id" name="machine_id" placeholder="Leave empty for current machine">
                    </div>
                    
                    <button type="submit" class="btn">Request License</button>
                </form>
                
                <div id="result" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <script>
            let selectedPackage = '';
            
            function selectPackage(packageName) {{
                selectedPackage = packageName;
                document.getElementById('package_name').value = packageName;
                
                // Update UI
                document.querySelectorAll('.package').forEach(p => p.classList.remove('selected'));
                event.target.closest('.package').classList.add('selected');
            }}
            
            async function submitRequest(event) {{
                event.preventDefault();
                
                const formData = new FormData(event.target);
                const data = Object.fromEntries(formData);
                
                if (!selectedPackage) {{
                    alert('Please select a package');
                    return;
                }}
                
                try {{
                    const response = await fetch('/api/request-license', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(data)
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        document.getElementById('result').innerHTML = `
                            <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px;">
                                <h3>✅ License Request Submitted!</h3>
                                <p>Request ID: ${{result.request_id}}</p>
                                <p>Your license will be sent to ${{data.email}} once approved.</p>
                            </div>
                        `;
                        event.target.reset();
                        selectedPackage = '';
                        document.querySelectorAll('.package').forEach(p => p.classList.remove('selected'));
                    }} else {{
                        throw new Error(result.detail || 'Request failed');
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = `
                        <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px;">
                            <h3>❌ Error</h3>
                            <p>${{error.message}}</p>
                        </div>
                    `;
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/request-license")
async def request_license(request: LicenseRequest):
    """Handle license requests"""
    try:
        request_id = str(uuid.uuid4())[:8]
        
        # Store request
        request_data = {
            "id": request_id,
            "email": request.email,
            "package_name": request.package_name,
            "intended_use": request.intended_use,
            "machine_id": request.machine_id,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }
        
        REQUEST_DB[request_id] = request_data
        
        # Send notification to admin
        admin_subject = f"New License Request - {request.package_name}"
        admin_body = f"""
        <h2>🔔 New License Request</h2>
        <p><strong>Request ID:</strong> {request_id}</p>
        <p><strong>Email:</strong> {request.email}</p>
        <p><strong>Package:</strong> {request.package_name}</p>
        <p><strong>Intended Use:</strong> {request.intended_use}</p>
        <p><strong>Machine ID:</strong> {request.machine_id or 'Not specified'}</p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <p><a href="http://localhost:8000/admin">Go to Admin Dashboard</a></p>
        """
        
        send_email(ADMIN_EMAIL, admin_subject, admin_body)
        
        # Send confirmation to user
        user_subject = f"License Request Received - {request.package_name}"
        user_body = f"""
        <h2>✅ License Request Received</h2>
        <p>Dear user,</p>
        <p>Your license request has been received and is being processed.</p>
        <p><strong>Request ID:</strong> {request_id}</p>
        <p><strong>Package:</strong> {request.package_name}</p>
        <p>You will receive your license file via email once approved.</p>
        <p>Thank you for choosing QuantumMeta!</p>
        """
        
        send_email(request.email, user_subject, user_body)
        
        return {"message": "License request submitted successfully", "request_id": request_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Admin dashboard for managing license requests"""
    
    # Get pending requests
    pending_requests = [req for req in REQUEST_DB.values() if req["status"] == "pending"]
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard - QuantumMeta License Server</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
            .card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .btn {{ background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
            .btn-success {{ background: #28a745; }}
            .btn-danger {{ background: #dc3545; }}
            .request-item {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; }}
            .status {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }}
            .status-pending {{ background: #fff3cd; color: #856404; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔐 Admin Dashboard</h1>
            <p>Manage license requests and approvals</p>
        </div>
        
        <div class="container">
            <div class="card">
                <h2>Pending License Requests ({len(pending_requests)})</h2>
                
                <div id="requests">
    """
    
    for request in pending_requests:
        html_content += f"""
                    <div class="request-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4>{request['package_name']} - {request['email']}</h4>
                                <p><strong>Request ID:</strong> {request['id']}</p>
                                <p><strong>Intended Use:</strong> {request['intended_use']}</p>
                                <p><strong>Machine ID:</strong> {request['machine_id'] or 'Not specified'}</p>
                                <p><strong>Time:</strong> {request['timestamp']}</p>
                                <span class="status status-pending">PENDING</span>
                            </div>
                            <div>
                                <button class="btn btn-success" onclick="approveRequest('{request['id']}')">Approve</button>
                                <button class="btn btn-danger" onclick="rejectRequest('{request['id']}')">Reject</button>
                            </div>
                        </div>
                    </div>
        """
    
    html_content += """
                </div>
            </div>
        </div>
        
        <script>
            async function approveRequest(requestId) {
                try {
                    const response = await fetch(`/api/admin/approve/${requestId}`, { method: 'POST' });
                    const result = await response.json();
                    
                    if (response.ok) {
                        alert('License approved and sent!');
                        location.reload();
                    } else {
                        alert('Error: ' + result.detail);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function rejectRequest(requestId) {
                if (confirm('Are you sure you want to reject this request?')) {
                    try {
                        const response = await fetch(`/api/admin/reject/${requestId}`, { method: 'POST' });
                        const result = await response.json();
                        
                        if (response.ok) {
                            alert('Request rejected');
                            location.reload();
                        } else {
                            alert('Error: ' + result.detail);
                        }
                    } catch (error) {
                        alert('Error: ' + error.message);
                    }
                }
            }
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.post("/api/admin/approve/{request_id}")
async def approve_request(request_id: str):
    """Approve a license request and generate license"""
    try:
        if request_id not in REQUEST_DB:
            raise HTTPException(status_code=404, detail="Request not found")
        
        request_data = REQUEST_DB[request_id]
        
        if request_data["status"] != "pending":
            raise HTTPException(status_code=400, detail="Request already processed")
        
        # Generate license file
        license_path = generate_license_file(request_data, request_id)
        
        if not license_path:
            raise HTTPException(status_code=500, detail="Failed to generate license")
        
        # Send license to user
        subject = f"Your {request_data['package_name']} License is Ready!"
        body = f"""
        <h2>🎉 License Approved!</h2>
        <p>Dear user,</p>
        <p>Your license for <strong>{request_data['package_name']}</strong> has been approved!</p>
        
        <h3>Installation Instructions:</h3>
        <ol>
            <li>Install the CLI tool: <code>pip install quantummeta-license</code></li>
            <li>Activate your license: <code>quantum-license activate {os.path.basename(license_path)}</code></li>
            <li>Import and use the package in your code</li>
        </ol>
        
        <p>Your license is valid for 1 year from today.</p>
        <p>Thank you for choosing QuantumMeta!</p>
        """
        
        if send_email(request_data["email"], subject, body, license_path):
            # Update request status
            REQUEST_DB[request_id]["status"] = "approved"
            REQUEST_DB[request_id]["approved_at"] = datetime.now().isoformat()
            
            # Clean up temporary file
            if os.path.exists(license_path):
                os.remove(license_path)
            
            return {"message": "License approved and sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send license email")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving request: {str(e)}")

@app.post("/api/admin/reject/{request_id}")
async def reject_request(request_id: str):
    """Reject a license request"""
    try:
        if request_id not in REQUEST_DB:
            raise HTTPException(status_code=404, detail="Request not found")
        
        request_data = REQUEST_DB[request_id]
        
        if request_data["status"] != "pending":
            raise HTTPException(status_code=400, detail="Request already processed")
        
        # Send rejection email
        subject = f"License Request Update - {request_data['package_name']}"
        body = f"""
        <h2>License Request Update</h2>
        <p>Dear user,</p>
        <p>Thank you for your interest in <strong>{request_data['package_name']}</strong>.</p>
        <p>Unfortunately, we cannot approve your license request at this time.</p>
        <p>If you have questions, please contact support.</p>
        """
        
        send_email(request_data["email"], subject, body)
        
        # Update request status
        REQUEST_DB[request_id]["status"] = "rejected"
        REQUEST_DB[request_id]["rejected_at"] = datetime.now().isoformat()
        
        return {"message": "Request rejected successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rejecting request: {str(e)}")

@app.post("/api/validate-license")
async def validate_license(validation: LicenseValidation):
    """Validate a license"""
    try:
        # This would integrate with the existing validation system
        # For now, return a basic response
        return {"valid": True, "message": "License validation endpoint"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

@app.get("/api/status/{email}")
async def check_status(email: str):
    """Check license status for an email"""
    try:
        user_requests = [req for req in REQUEST_DB.values() if req["email"] == email]
        return {"requests": user_requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.1.1", "server": "QuantumMeta License Server"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
