using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace prjVerano.Forms
{
    public partial class frmEmployeeDE : Form
    {
        public int EmployeeId { get; set; }
        public bool IsEdit { get; set; }

        public frmEmployeeDE()
        {
            EmployeeId = 0;
            IsEdit = false;

            InitializeComponent();
        }

        public frmEmployeeDE(int empId, bool isEdit)
        {
            EmployeeId = empId;
            IsEdit = IsEdit;

            InitializeComponent();
        }

        private void frmEmployeeDE_Load(object sender, EventArgs e)
        {

        }
    }
}
