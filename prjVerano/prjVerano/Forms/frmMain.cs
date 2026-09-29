using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Net.Http;
using System.Threading.Tasks;
using System.Windows.Forms;
using prjVerano.Forms;
using prjVerano.Models;

namespace prjVerano
{
    public partial class frmMain : Form
    {
        private readonly HttpClient client = new HttpClient();
        private const string BASE_URL = "http://127.0.0.1:5000/employees";

        public frmMain()
        {
            InitializeComponent();
        }

        private void btnNew_Click(object sender, EventArgs e)
        {
            new frmEmployeeDE().ShowDialog();
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            if (dgvEmployees.CurrentRow == null)
            {
                MessageBox.Show("Select a record to edit.");
                return;
            }

            int empId = Convert.ToInt32(dgvEmployees.CurrentRow.Cells["id"].Value);

            new frmEmployeeDE(empId, true).ShowDialog();
        }

        private void frmMain_Load(object sender, EventArgs e)
        {

        }

        private async Task LoadEmployees()
        {
            HttpResponseMessage response = await client.GetAsync(BASE_URL);
            string json = await response.Content.ReadAsStringAsync();

            if (response.IsSuccessStatusCode)
            {
                dgvEmployees.DataSource = JsonSerializer.Deserialize<List<Employee>>(json);

            }
            else
            {
                string message 
                MessageBox.Show("Unable to employees.");
            }

            

        }

        private void btnDelete_Click(object sender, EventArgs e)
        {

        }
    }
}
