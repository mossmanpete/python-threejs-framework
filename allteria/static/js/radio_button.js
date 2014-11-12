
// @author theom / https://www.axonehf.com

allteria.radio_button = function radio_button(label)
{
    allteria.ui_component.call(this);

    this.outer_radius = 4;
    this.inner_radius = 3.5;
    this.bullet_radius = 2;
    this.set_scale(3);
    this.checked = false;

    var geo;
    var mat;
    
    this.label = new allteria.text_line(label, this.scale.x / 2.3);
    this.label.translateX(-(this.label.get_width() + this.outer_radius));
    this.add(this.label);

    var segments = 16;

    geo = new three.CircleGeometry(this.bullet_radius, segments);
    mat = new three.MeshBasicMaterial({color: 0x000000});
    this.bullet = new three.Mesh(geo, mat);
    this.bullet.comp = this;
    this.bullet.visible = this.checked;
    this.add(this.bullet);

    geo = new three.CircleGeometry(this.inner_radius, segments);
    mat = new three.MeshBasicMaterial({color: 0xffffff});
    this.background = new three.Mesh(geo, mat);
    this.background.comp = this;
    this.add(this.background);

    geo = new three.CircleGeometry(this.outer_radius, segments);
    mat = new three.MeshBasicMaterial({color: 0x000000});
    this.border = new three.Mesh(geo, mat);
    this.add(this.border);
}

allteria.extend(allteria.radio_button, allteria.ui_component);

allteria.radio_button.prototype.set_position = function set_position(pos)
{
    this.position.set(pos.x, pos.y, pos.z);
}

allteria.radio_button.prototype.get_position = function get_position()
{
    return this.position;
}

allteria.radio_button.prototype.set_scale = function set_scale(s)
{
    this.scale.x = s;
    this.scale.y = s;
}

allteria.radio_button.prototype.get_scale = function get_scale()
{
    return this.scale.x;
}

// This method gets overridden by the group
allteria.radio_button.prototype.on_mouse_down = function on_mouse_down(event)
{
    this.check(event);
}

allteria.radio_button.prototype.check = function check(event)
{
    if (!this.checked)
    {
        this.checked = true;
        this.bullet.visible = true;
        this.on_checked(event);
    }
}

allteria.radio_button.prototype.uncheck = function uncheck(event)
{
    if (this.checked)
    {
        this.checked = false;
        this.bullet.visible = false;
        this.on_unchecked(event)
    }
}

allteria.radio_button.prototype.on_checked = function on_checked(event)
{
}

allteria.radio_button.prototype.on_unchecked = function on_unchecked(event)
{
}

allteria.radio_button.prototype.set_editable = function set_editable(editable)
{
    this.label.set_editable(editable);
}
